from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import uuid

# LangGraph workflow
from graph.workflow import graph

# Database
from database.connection import SessionLocal, engine, Base
from database.crud import save_query_history, get_last_5_queries
from database.schemas import QueryHistoryResponse


# -------------------------------
# INIT APP
# -------------------------------
app = FastAPI(title="DocMind API")

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables
Base.metadata.create_all(bind=engine)

# upload folder
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------------
# DB DEPENDENCY
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# ASK ENDPOINT
# -------------------------------
@app.post("/ask")
async def ask_question(
    file: UploadFile = File(...),
    user_question: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # unique filename
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # save uploaded file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # LangGraph invoke
        result = graph.invoke({
            "file_path": file_path,
            "question": user_question
        })

        # extract answer only
        answer = result.get("answer", "No answer generated")

        # save history in DB
        save_query_history(
            db=db,
            filename=file.filename,
            question=user_question,
            response=answer
        )

        return {
            "filename": file.filename,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# HISTORY ENDPOINT
# -------------------------------
@app.get("/history", response_model=list[QueryHistoryResponse])
def get_history(db: Session = Depends(get_db)):
    return get_last_5_queries(db)


# -------------------------------
# HEALTH CHECK
# -------------------------------
@app.get("/")
def root():
    return {"message": "DocMind API is running 🚀"}