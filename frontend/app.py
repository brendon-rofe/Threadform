import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

load_dotenv()

if "threads" not in st.session_state:
    st.session_state.threads = {"Default": []}
    st.session_state.current_thread = "Default"

def generate_response(prompt):
    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=[{"role": "user", "parts": [{"text": prompt}]}]
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text

st.sidebar.title("Threads")

thread_names = list(st.session_state.threads.keys())
selected_thread = st.sidebar.selectbox("Select a thread", thread_names, index=thread_names.index(st.session_state.current_thread))

new_thread_name = st.sidebar.text_input("New thread name")
if st.sidebar.button("Create thread") and new_thread_name:
    if new_thread_name not in st.session_state.threads:
        st.session_state.threads[new_thread_name] = []
        st.session_state.current_thread = new_thread_name
        st.rerun()

if selected_thread != st.session_state.current_thread:
    st.session_state.current_thread = selected_thread
    st.rerun()

st.title(f"Threadform: {st.session_state.current_thread}")

messages = st.session_state.threads[st.session_state.current_thread]

for role, msg in messages:
    with st.chat_message(role):
        st.markdown(msg)

prompt = st.chat_input("Ask anything")

if prompt:
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    response_chunks = []

    def stream_and_store():
        for chunk in generate_response(prompt):
            response_chunks.append(chunk)
            yield chunk

    st.write_stream(stream_and_store())

    full_response = "".join(response_chunks)
    st.session_state.threads[st.session_state.current_thread].append(("assistant", full_response))

