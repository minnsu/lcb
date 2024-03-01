from langchain.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

default_embedding_model_path = '/workspace/llms/all-MiniLM-L6-v2'

def get_vector_DB(db_path: str, embedding_model_path: str=None):
    if embedding_model_path is None:
        embedding_model_path = default_embedding_model_path
    
    embedding_function = SentenceTransformerEmbeddings(model_name=embedding_model_path)
    db = Chroma(persist_directory=db_path, embedding_function=embedding_function)

    return db

# Information load and store
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