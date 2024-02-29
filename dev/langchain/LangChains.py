import torch
import langchain

if torch.cuda.is_available():
    torch.set_default_device('cuda')

# LLM pipe node
from transformers import pipeline, AutoModel, AutoModelForCausalLM, AutoTokenizer
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

def get_model_and_tokenizer(model_path, load_in_8bit: bool=False):
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto', torch_dtype=torch.bfloat16, load_in_8bit=load_in_8bit)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return (model, tokenizer)
    

def make_llm_pipe(model_path: str, task: str, max_new_tokens: int=512, temperature: float=0.6, top_p: float=0.95, repetition_penalty: float=1.2, load_in_8bit: bool=False):
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto', torch_dtype=torch.bfloat16, load_in_8bit=load_in_8bit)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    hf_pipe = pipeline(task=task, model=model, tokenizer=tokenizer, max_new_tokens=max_new_tokens, do_sample=True, temperature=temperature, top_p=top_p, repetition_penalty=repetition_penalty)
    lc_pipe = HuggingFacePipeline(pipeline=hf_pipe)
    return lc_pipe

def make_llm_pipe_fast(model_path: str, task: str, max_new_tokens: int=512, temperature: float=0.6, top_p: float=0.95, repetition_penalty: float=1.2):
    lc_pipe = HuggingFacePipeline.from_model_id(
        model_id=model_path,
        device=0,
        task=task,
        pipeline_kwargs={
            'max_new_tokens': max_new_tokens,
            'do_sample': True,
            'temperature': temperature,
            'top_p': top_p,
            'repetition_penalty': repetition_penalty
        }
    )
    return lc_pipe

# Prompt pipe node
from langchain.prompts import PromptTemplate #, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
# from langchain.schema import HumanMessage, SystemMessage

from langchain.chains import ConversationChain, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from File import save_memory, load_memory

def make_default_prompt():
    template = """
Your Role: {role}
------------------
Background knowledge: {context}
------------------
Chat history: {history}
------------------
Question: {input}
------------------
Answer:
"""
    prompt = PromptTemplate(input_variables=['role', 'context', 'history', 'input'], template=template)
    return prompt

def make_chain(llm, db_for_retriever, prompt=None, memory_path=None, verbose=False):
    if prompt is None:
        prompt = make_default_prompt()
    
    if memory_path is None:
        memory = ConversationBufferMemory(memory_key='history', return_messages=True)
    else:        
        memory = load_memory(memory_path)
    
    chain = ConversationalRetrievalChain(
        llm=llm,
        retreiver=db_for_retriever.as_retriever(),
        verbose=verbose,
        memory=memory,
    )
    return (prompt | chain)
    # TODO: chain 연결이 이상해요! role은 고정한다고 해도, context를 db에서, history를 memory에서 받아오는 chain을 구성해야 해요!

# Make or load vector DB
from langchain.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

default_embedding_model_path = '/workspace/llms/all-MiniLM-L6-v2'

def get_vector_DB(db_path: str, embedding_model_path: str=None):
    if embedding_model_path is None:
        embedding_model_path = default_embedding_model_path
    
    embedding_function = SentenceTransformerEmbeddings(model_name=embedding_model_path)
    db = Chroma(persist_directory=db_path, embedding_function=embedding_function)

    return db


# Information storing
from langchain.document_loaders import WebBaseLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

DEFAULT_CHUNK_SIZE=1024
DEFAULT_CHUNK_OVERLAP=128

def split_docs_from_loader(loader, chunk_size, chunk_overlap):
    raw_doc = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(raw_doc)

def docs_from_url(url: str, chunk_size: int=DEFAULT_CHUNK_SIZE, chunk_overlap: int=DEFAULT_CHUNK_OVERLAP):
    loader = WebBaseLoader(url)
    return split_docs_from_loader(loader, chunk_size, chunk_overlap)

def docs_from_txt(path: str, chunk_size: int=DEFAULT_CHUNK_SIZE, chunk_overlap: int=DEFAULT_CHUNK_OVERLAP):
    loader = TextLoader(path)
    return split_docs_from_loader(loader, chunk_size, chunk_overlap)

def docs_from_pdf(path: str):
    loader = PyPDFLoader(path)
    return loader.load_and_split()

def store_docs(db, docs):
    db.add_documents(docs)