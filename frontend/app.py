import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

load_dotenv()

def generate_response(prompt):
    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=[{"role": "user", "parts": [{"text": prompt}]}]
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text

st.title("Threadform MVP")

prompt = st.chat_input("Ask anything")

if prompt:
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    st.write_stream(generate_response(prompt))
