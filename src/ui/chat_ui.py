import streamlit as st
from src.llm.model import ModelRunner

def chat_ui(messages:list[dict],model:ModelRunner,append_message=None):
    st.title("Streamlit Chatbot Interface")
    st.write("Welcome to the document search engine. You can upload a PDF document to be processed by the model.")


    USER_AVATAR = "👤"
    BOT_AVATAR = "🤖"

    # Display chat messages
    for message in messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Main chat interface
    if prompt := st.chat_input("How can I help?"):
        # st.session_state.messages.append({"role": "user", "content": prompt})
        if append_message is not None:
            append_message({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()

            full_response = ""
            
            for response in model.ask_stream(prompt):
                full_response += response.get("answer","")
                message_placeholder.markdown(full_response + "|")

            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # # Save chat history after each interaction
    # save_chat_history(st.session_state.messages)
