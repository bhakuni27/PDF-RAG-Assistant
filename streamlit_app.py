import streamlit as st
from src.app import DocQAAssistant

st.set_page_config(page_title="Doc QA Assistant", page_icon="📄", layout="wide")

st.title("📄 Document Question Answering Assistant")

# Store chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "assistant" not in st.session_state:
    st.session_state.assistant = None

def handle_question():
    question = st.session_state.user_input.strip()
    if question:
        answer, retrieved_chunks = st.session_state.assistant.answer_question(question)
        st.session_state.chat_history.append({
            "question": question,
            "answer": answer,
            "context": retrieved_chunks
        })
        # clear the input box
        st.session_state.user_input = ""

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    if st.session_state.assistant is None:
        st.session_state.assistant = DocQAAssistant(uploaded_file)

    st.success("✅ Document processed. Ask me questions!")

    # Custom CSS for chat bubbles
    st.markdown(
        """
        <style>
        .user-bubble {
            background-color: #DCF8C6;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: right;
        }
        .assistant-bubble {
            background-color: #F1F0F0;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Show previous Q&A
    for qa in st.session_state.chat_history:
        st.markdown(f"<div class='user-bubble'><b>You:</b> {qa['question']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='assistant-bubble'><b>Assistant:</b> {qa['answer']}</div>", unsafe_allow_html=True)

        # Retrieved context chunks
        with st.expander("📌 Retrieved Context"):
            for idx, chunk in enumerate(qa["context"], 1):
                st.markdown(f"**Chunk {idx}:** {chunk}")

    # Input for new question, handled by callback
    st.text_input(
        "Enter your question:",
        key="user_input",
        on_change=handle_question
    )
