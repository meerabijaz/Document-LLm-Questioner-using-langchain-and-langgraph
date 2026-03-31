from sqlalchemy.orm import Session
from database.models import QueryHistory


def save_query_history(
    db: Session,
    filename: str,
    question: str,
    response: str
):
    record = QueryHistory(
        filename=filename,
        question=question,
        response=response
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_last_5_queries(db: Session):
    return (
        db.query(QueryHistory)
        .order_by(QueryHistory.created_at.desc())
        .limit(5)
        .all()
    )