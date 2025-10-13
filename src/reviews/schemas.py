from pydantic import BaseModel, Field
import uuid
from typing import Optional
from datetime import datetime

class ReviewModel(BaseModel):
    uid: uuid.UUID
    review_text: str
    rating: int = Field(lt=5)
    book_uid: Optional[uuid.UUID]
    user_uid: Optional[uuid.UUID]
    created_at: datetime
    update_at: datetime


class ReviewCreateModel(BaseModel):
    review_text: str
    rating: int = Field(lt=5)