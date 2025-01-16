from langchain.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings

class DocDb:
    
    def __init__(self, path):
        self.path = path
        # self.vector_store = Chroma(persist_directory=path,embedding_function=OllamaEmbeddings('nomic-embed-text:latest'))
        
        self.vector_store = Chroma(embedding_function=OllamaEmbeddings(model="nomic-embed-text:latest"), persist_directory=path)
    
    def add_document(self, doc):
        self.vector_store.add_documents(doc)

    def search(self, query):
        return self.vector_store.similarity_search(query)
    
    def save(self):
        self.vector_store.save(self.path)
    
    def close(self):
        self.vector_store.close()