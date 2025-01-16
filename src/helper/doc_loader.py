from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class DocLoader:
    @staticmethod
    def load_pdf(path):
        # Check if the given path exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file at path {path} does not exist.")

        try:
            # loading file
            pdf = PyMuPDFLoader(path)
            docs = pdf.load()

            # Splitting the document into chunks
            return DocLoader.__split_docs__(docs)
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the PDF: {e}")

    @staticmethod
    def __split_docs__(docs):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1400, chunk_overlap=200)
        return splitter.split_documents(docs)
