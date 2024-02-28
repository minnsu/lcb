import torch
import langchain

# LLM pipe node
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

def make_llm_pipe(model_path: str, task: str, max_new_tokens: int=512, temperature: float=0.6, top_p: float=0.95, repetition_penalty: float=1.2, load_in_8bit: bool=True):
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto', torch_dtype=torch.float16, load_in_8bit=load_in_8bit)
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
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage

default_roles = """You having a chat with human. Always answer shortly based on your knowledge."""
def make_role(template=None):
    if template is None:
        role = SystemMessagePromptTemplate.from_template(default_roles)
    else:
        role = SystemMessagePromptTemplate.from_template(template)
    return role

def make_human_message():
    return HumanMessagePromptTemplate.from_template("""{text}""")

def make_message(text):
    role_template = make_role()
    human_template = make_human_message()
    chat_prompt = ChatPromptTemplate.from_messages(
        [role_template, human_template]
    )
    chat_message = chat_prompt.format_prompt(
        text=text
    )
    return chat_message.to_messages()

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from File import save_memory, load_memory

def make_default_prompt():
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessage(default_roles),
            MessagesPlaceholder(variable_name='history'),
            HumanMessagePromptTemplate.from_template('{input}')
        ],
    )
    return prompt

def make_chain(llm, prompt=None, memory_path=None, verbose=True):
    if prompt is None:
        prompt = make_default_prompt()
    
    if memory_path is None:
        memory = ConversationBufferMemory(memory_key='history', return_messages=True)
    else:        
        memory = load_memory(memory_path)
    
    chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        verbose=verbose,
        memory=memory,
    )
    return chain