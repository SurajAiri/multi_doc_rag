from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from pathlib import Path

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
    def load_pdf_bytes(file_path, pdf_bytes):
        try:
            # id = uuid.uuid4()
            if os.path.exists(file_path):
                raise FileExistsError(f"The file at path {file_path} already exists.")
            
            
            # save the pdf file
            with open(file_path, "wb") as f:
                f.write(pdf_bytes)
            
            # loading file
            pdf = PyMuPDFLoader(file_path)
            docs = pdf.load()

            # Splitting the document into chunks
            return DocLoader.__split_docs__(docs)
        except FileExistsError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the PDF: {e}")

    # Todo: Check this approach later for the implementation with langchain  
    # # Read the PDF from bytes
    # import fitz  # PyMuPDF
    # pdf_document = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")

    # # Extract text from each page
    # text = ""
    # for page_num in range(len(pdf_document)):
    #     page = pdf_document.load_page(page_num)
    #     text += page.get_text()

    @staticmethod
    def __split_docs__(docs):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1400, chunk_overlap=200)
        return splitter.split_documents(docs)
