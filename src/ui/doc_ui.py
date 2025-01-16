import streamlit as st

from src.helper.doc_db import DocDb
from src.helper.doc_loader import DocLoader

def upload_pdf_ui(db:DocDb,on_upload=None,on_back=None):
    st.header("Document Uploader")
    st.write("Upload a PDF document to be processed by the model.")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    # st.button(label="Back",on_click=on_back) 
    if uploaded_file is not None:
        st.write("File uploaded successfully.")
        try:
            st.write("Processing the document...")
            docs = DocLoader.load_pdf_bytes(uploaded_file.name,uploaded_file.getvalue())
            st.write("Encoding and adding the document to the database...")
            # Add the documents to the database
            db.add_document(docs)
            st.write("Document added to the database.")
            st.button(label="Continue",on_click=on_back)
        except FileExistsError as e:
            st.markdown("## The file already exists. and the document is already in the database.")
            st.button(label="Back",on_click=on_back)
        except Exception as e:
            st.write("An error occurred while processing the document.")
            st.write(e)
            st.button(label="Back",on_click=on_back)

    else:
        st.button(label="Back",on_click= on_back)
        
    