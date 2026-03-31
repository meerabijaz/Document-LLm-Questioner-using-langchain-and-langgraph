from langgraph.graph import StateGraph, START, END
from graph.state import GraphState
from graph.nodes import (
    greeting_node,
    document_qa_node,
    route_question
)

builder = StateGraph(GraphState)

builder.add_node("greeting", greeting_node)
builder.add_node("document_qa", document_qa_node)

builder.add_conditional_edges(
    START,
    route_question,
    {
        "greeting": "greeting",
        "document_qa": "document_qa"
    }
)

builder.add_edge("greeting", END)
builder.add_edge("document_qa", END)

graph = builder.compile()