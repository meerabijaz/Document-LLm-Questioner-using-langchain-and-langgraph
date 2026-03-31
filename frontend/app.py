import streamlit as st
import requests
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DocMind · RAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- SESSION ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_history" not in st.session_state:
    st.session_state.selected_history = None


# ---------- HELPERS ----------
def fmt_time(ts: str) -> str:
    try:
        return datetime.fromisoformat(ts).strftime("%b %d · %H:%M")
    except Exception:
        return ts


@st.cache_data(ttl=5)
def fetch_history():
    try:
        r = requests.get(f"{BACKEND_URL}/history", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return []


def ask_backend(file_bytes: bytes, filename: str, question: str):
    try:
        files = {"file": (filename, file_bytes)}
        data = {"user_question": question}
        r = requests.post(f"{BACKEND_URL}/ask", files=files, data=data, timeout=120)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


# ---------- SIDEBAR ----------
st.sidebar.title("🧠 DocMind")
st.sidebar.caption("Recent queries")

history = fetch_history()

if history:
    for i, item in enumerate(history):
        label = item.get("question", "Untitled")[:40]
        meta = f"📄 {item.get('filename', '-') } · {fmt_time(item.get('created_at', ''))}"
        if st.sidebar.button(label, key=f"hist_{i}", use_container_width=True, help=meta):
            # Load selected history into chat view
            st.session_state.selected_history = item
            st.session_state.messages = [
                {"role": "user", "content": item.get("question", "")},
                {"role": "assistant", "content": item.get("response", "")},
            ]
            # No manual rerun needed; Streamlit reruns automatically on button click
else:
    st.sidebar.info("No history yet")

st.sidebar.divider()
st.sidebar.caption(f"Backend: {BACKEND_URL}")


# ---------- MAIN ----------
st.title("📄 Ask your documents")
st.caption("Upload a file and chat with it like ChatGPT")

uploaded_file = st.file_uploader(
    "Upload document",
    type=["pdf", "docx", "txt", "csv"],
)

question = st.chat_input("Ask something about your document...")

# render existing conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# new question flow
if question:
    if not uploaded_file:
        st.error("Please upload a document first.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = ask_backend(
                    uploaded_file.read(),
                    uploaded_file.name,
                    question,
                )

                if "error" in result:
                    st.error(result["error"])
                else:
                    answer = result.get("answer", "No answer returned")
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                    fetch_history.clear()
