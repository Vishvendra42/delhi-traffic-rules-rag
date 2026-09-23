import streamlit as st
import requests

API_URL = "https://delhi-traffic-rules-rag.onrender.com/ask"

st.set_page_config(
    page_title="Delhi Traffic Assistant",
    page_icon="🚦",
    layout="centered"
)

# -----------------------------
# Header
# -----------------------------
st.title("🚦 Delhi Traffic Assistant")
st.caption("AI-powered assistant for Delhi traffic rules, penalties and road safety")


# -----------------------------
# API Status
# -----------------------------
try:
    response = requests.get(f"{API_URL}/", timeout=3)

    if response.status_code == 200:
        st.success("API: Online")
    else:
        st.error("API: Offline")

except requests.exceptions.RequestException:
    st.error("API: Offline")


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("💡 Try asking")

    sample_questions = [
        "What is the fine for driving without a licence?",
        "What is the fine for not wearing a helmet?",
        "What is the fine for not wearing a seat belt?",
        "What documents should I carry while driving in Delhi?",
        "What is the fine for triple riding on a two-wheeler?",
        "What are the speed limits in Delhi?"
    ]

    for question in sample_questions:

        if st.button(
            question,
            key=f"sample_{question}",
            use_container_width=True
        ):
            st.session_state.selected_question = question


# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Display Previous Messages
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Input
# -----------------------------
question = st.chat_input(
    "Ask about Delhi traffic rules..."
)


# If sidebar question was selected
if "selected_question" in st.session_state:

    question = st.session_state.selected_question
    del st.session_state.selected_question


# -----------------------------
# Process Question
# -----------------------------
if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Get response from backend
    try:

        with st.spinner("Searching Delhi traffic rules..."):

            response = requests.post(
                f"{API_URL}/ask",
                json={
                    "query": question,
                    "top_k": 5
                },
                timeout=60
            )

        if response.status_code == 200:

            data = response.json()

            answer = data.get(
                "answer",
                data.get(
                    "response",
                    "No answer received from the API."
                )
            )

        else:

            answer = f"API Error: {response.status_code}"

    except requests.exceptions.RequestException as e:

        answer = f"Could not connect to the API: {e}"

    # Assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)