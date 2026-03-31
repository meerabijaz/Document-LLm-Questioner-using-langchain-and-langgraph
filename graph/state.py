from typing_extensions import TypedDict


class GraphState(TypedDict):
    file_path: str
    question: str
    answer: str