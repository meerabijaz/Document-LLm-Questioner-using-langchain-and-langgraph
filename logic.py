from documentProcessor import (
    load_documents,
    split_documents,
    create_vector_store,
    search_documents
)

from prompt_Builder import build_prompt
from llmservice import ask_groq


def process_query(files, user_question):
    try:
        # 1) Load docs
        docs = load_documents(files)
        if not docs:
            return "No readable content found in the document."

        # 2) Split docs
        splits = split_documents(docs)
        if not splits:
            return "Document could not be processed into chunks."

        # 3) Create FAISS
        vector_db = create_vector_store(splits)

        # 4) Retrieve relevant chunks
        results = search_documents(vector_db, user_question)

        if not results:
            return "No relevant information found in document."

        # 5) Build context
        context = "\n\n".join([doc.page_content for doc in results])

        # 6) Build prompt
        prompt = build_prompt(context, user_question)

        # 7) Ask LLM
        answer = ask_groq(prompt)

        return str(answer) if answer else "No answer generated."

    except Exception as e:
        print("❌ PROCESS_QUERY ERROR:", str(e))  # 🔥 critical
        return f"Error processing document: {str(e)}"