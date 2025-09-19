# chatbot_streamlit.py
import streamlit as st
import requests

st.set_page_config(page_title="HR Policy Chatbot", layout="centered")

st.title("📘 HR Policy Chatbot")

# Input for API URL
api_url = st.text_input(
    "Backend API URL",
    "http://127.0.0.1:8000/query",
    help="Enter your FastAPI backend endpoint"
)

# ✅ Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input box
query = st.text_input("Ask a question about the HR Policy:")

if st.button("Send"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        try:
            response = requests.post(api_url, json={"query": query})
            if response.status_code == 200:
                data = response.json()

                # Add to chat history
                st.session_state.chat_history.append({
                    "question": query,
                    "answer": data["answer"],
                    "sources": data.get("sources", [])
                })
            else:
                st.error(f"API error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")

# ✅ Display full chat history
if st.session_state.chat_history:
    for i, chat in enumerate(st.session_state.chat_history, 1):
        st.markdown(f"### ❓ Q{i}: {chat['question']}")
        st.markdown(f"**✅ Answer:** {chat['answer']}")

        if chat["sources"]:
            st.markdown("**📌 Sources:**")
            for s in chat["sources"]:
                st.markdown(f"- Page {s['page']}: {s['snippet']}")
        st.markdown("---")