import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("key")

st.set_page_config(page_title="Gemini Chatbot")
st.title("Gemini Chatbot")

ll= ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=key
)

storage = ConversationBufferMemory(return_messages=True)

conversation = ConversationChain(
    llm=ll,
    memory=storage
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = msg["role"]
    with st.chat_message(role):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = conversation.run(user_input)

    with st.chat_message("AI"):
        st.markdown(response)

    st.session_state.messages.append({"role": "AI", "content": response})
