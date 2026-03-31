import os
from langchain_groq import ChatGroq
import os
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None
)

def ask_groq(prompt: str):
    response = llm.invoke(prompt)
    return response.contentcls
