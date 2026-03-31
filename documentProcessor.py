import os
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    PDFPlumberLoader,   # ✅ appended
    Docx2txtLoader,
    TextLoader,
    CSVLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# -------------------------------
# 1) LOAD MULTIPLE DOCUMENT TYPES
# -------------------------------
def load_documents(file_paths: List[str]):
    """
    Load documents from multiple supported file types.
    Supported: pdf, docx, txt, csv
    """
    all_docs = []

    for file_path in file_paths:
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            try:
                # ✅ Better for invoices, tables, receipts
                loader = PDFPlumberLoader(file_path)
            except Exception:
                # fallback
                loader = PyPDFLoader(file_path)

        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)

        elif ext == ".txt":
            loader = TextLoader(file_path)

        elif ext == ".csv":
            loader = CSVLoader(file_path)

        else:
            raise ValueError(f"Unsupported file type: {ext}")

        docs = loader.load()

        # ✅ remove empty pages
        valid_docs = [doc for doc in docs if doc.page_content.strip()]

        print(f"📄 Loaded {len(valid_docs)} valid pages from {file_path}")

        all_docs.extend(valid_docs)

    return all_docs


# -------------------------------
# 2) CHUNK DOCUMENTS
# -------------------------------
def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Split documents into chunks for embeddings.
    """
    if not documents:
        print("⚠️ No valid documents found for splitting")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    splits = splitter.split_documents(documents)

    print(f"✂️ Created {len(splits)} chunks")

    return splits


# -------------------------------
# 3) CREATE / SAVE VECTOR DB
# -------------------------------
def create_vector_store(splits, db_path="faiss_index"):
    """
    Create FAISS vector database and save locally.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local(db_path)

    return vectorstore


# -------------------------------
# 4) SEARCH VECTOR DB
# -------------------------------
def search_documents(vectorstore, query: str, k=3):
    """
    Retrieve top-k relevant chunks.
    """
    return vectorstore.similarity_search(query, k=k)