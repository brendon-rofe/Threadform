import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

st.title("Threadform")

prompt = st.chat_input("Ask anything")

if prompt:
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    st.write(f"The user entered the following prompt: {prompt}")
