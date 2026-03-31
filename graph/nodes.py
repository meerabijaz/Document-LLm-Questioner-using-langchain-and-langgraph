from graph.state import GraphState
from logic import process_query
from parsers.responseparser import clean_llm_response

def greeting_node(state: GraphState):
    return {
        "answer": "Hello 👋 How can I help you with your document today?"
    }




def document_qa_node(state):
    raw_answer = process_query(
        [state["file_path"]],
        state["question"]
    )

    clean_answer = clean_llm_response(raw_answer)

    return {"answer": clean_answer}
def route_question(state):
    q = state["question"].lower().strip()

    greeting_words = {
        "hi",
        "hy",
        "hello",
        "hey",
        "salam",
        "assalamualaikum"
    }

    # exact greeting
    if q in greeting_words:
        return "greeting"

    # greeting at start only
    first_word = q.split()[0] if q.split() else ""

    if first_word in greeting_words:
        return "greeting"

    return "document_qa"