from langchain.prompts import PromptTemplate #, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chains import ConversationChain, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from lc_package.utils import save_memory, load_memory

default_role = """Use the following pieces of context and chat history to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Don't be wordy, just answer what is asked."""

default_template = """
Your Role: {role}

[Context]
{context}

[Chat history]
{chat_history}

Question: {question}

Helpful Answer:
"""

def default_prompt():
    return PromptTemplate.from_template(template=default_template)

def make_llm_chain(llm, prompt=None):
    if prompt is None:
        prompt = default_prompt()
    return (prompt | llm)

def make_context(db, text, limit: int=10):
    searched = db.similarity_search(text)
    str_searched = ''
    for i in range(min(len(searched), limit)):
        str_searched += searched[i].page_content
    return str_searched

def make_history(memory):
    return memory.buffer_as_str # memory: ConversationBufferMemory

def invoke(llm_chain, db, memory, question, role: str=None):
    if role is None:
        role = default_role
    ret = llm_chain.invoke({'role': role, 'context': make_context(db, question), 'chat_history': make_history(memory), 'question': question})

    memory.buffer_as_messages.append(HumanMessage(question))
    memory.buffer_as_messages.append(AIMessage(ret))
    
    return ret