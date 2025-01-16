from src.helper.doc_db import DocDb
from src.helper.doc_loader import DocLoader
from src.llm.model import ModelRunner
from src.ui.chat_ui import chat_ui
from src.ui.doc_ui import upload_pdf_ui
import streamlit as st
import shelve

DB_PATH = "output/db/chroma"
CHAT_PATH = "output/chat_history"

def set_view_page(page:str):
    st.session_state.view_page = page

# Load chat history from shelve file
def load_chat_history():
    with shelve.open(CHAT_PATH) as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open(CHAT_PATH) as db:
        db["messages"] = messages

def append_message(message):
    st.session_state.messages.append(message)
    save_chat_history(st.session_state.messages)

def main():
    db = DocDb(DB_PATH)
    model = ModelRunner(db)

    # states
    # View page
    if 'view_page' not in st.session_state:
        st.session_state.view_page = 'home'
    # Initialize or load chat history
    if "messages" not in st.session_state:
        st.session_state.messages = load_chat_history()

    # st.title("Document Search Engine 📚 ")

    # Sidebar with a button to delete chat history
    with st.sidebar:
        if st.button("Delete Chat History"):
            st.session_state.messages = []
            save_chat_history([])

        if st.session_state.view_page != 'home':
            st.button('Home',on_click=lambda: set_view_page('home'))
            
        if st.session_state.view_page != 'upload_doc':
            st.button('Upload Document',on_click=lambda: set_view_page('upload_doc'))

    
    # Navigation
    if 'upload_doc' == st.session_state.view_page:
        upload_pdf_ui(db,on_back=lambda: set_view_page('home'))
    else:
        chat_ui(
            messages=st.session_state.messages,
            model=model,
            append_message=append_message)

if __name__ == "__main__":
    main()