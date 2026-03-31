from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ✅ base shared fields
class QueryHistoryBase(BaseModel):
    filename: Optional[str] = None
    question: str
    response: str


# ✅ for creating records
class QueryHistoryCreate(QueryHistoryBase):
    pass


# ✅ for API responses
class QueryHistoryResponse(QueryHistoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True