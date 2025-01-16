
from src.llm.prompts import PDF_PROMPT
from src.helper.doc_db import DocDb
from langchain.vectorstores import Chroma
from langchain_ollama.chat_models import ChatOllama

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

class ModelRunner:
    def __init__(self, doc_db=None, path=None):
        if doc_db is not None:
            self.doc_db = doc_db
        elif path is not None:
            self.doc_db = DocDb(path)
        else:
            raise ValueError("Either doc_db or path must be provided")
        retriever = self.doc_db.vector_store.as_retriever()
        model = ChatOllama(model='phi3.5', temperature=0.4)
        mdl = create_stuff_documents_chain(model, prompt=PDF_PROMPT)
        self.chain = create_retrieval_chain(retriever, mdl)

    def ask(self, question):
        return self.chain.invoke({"input": question})
    
    def ask_stream(self, question):
        return self.chain.stream({'input':question})
        
    
