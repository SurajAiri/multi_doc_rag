import streamlit as st
from dotenv import load_dotenv
import shelve
from langchain_ollama import ChatOllama

load_dotenv()

st.title("Streamlit Chatbot Interface")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"


# Initialize Ollama model
model = ChatOllama(model='phi3.5', temperature=0.4)
# model = ChatOllama(model="hf.co/SicariusSicariiStuff/Phi-3.5-mini-instruct_Uncensored_GGUFs:Q4_K_M", temperature=0.4)

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

if "visibility" not in st.session_state:
    st.session_state.visibility = True

# Sidebar with a button to delete chat history
with st.sidebar:
    # Model selection
    # selected_model = st.selectbox("Select Ollama Model", model)
    # model = ChatOllama(model=selected_model)

    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

    if st.button('toggle view'):
        st.session_state.visibility = not st.session_state.visibility
        print("we got called",st.session_state.visibility)

if st.session_state.visibility:

    # Display chat messages
    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Main chat interface
    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()

            full_response = ""
            
            for response in model.stream(prompt):
                full_response += response.content
                message_placeholder.markdown(full_response + "|")
                
            

            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Save chat history after each interaction
    save_chat_history(st.session_state.messages)

else:
    st.write("Nothing to show")