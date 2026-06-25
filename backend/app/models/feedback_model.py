from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from app.models.question_model import PyObjectId

class FeedbackCreate(BaseModel):
    question_id: str = Field(..., alias="questionId")
    predicted_topic: str = Field(..., alias="predictedTopic")
    correct_topic: str = Field(..., alias="correctTopic")
    rating: str = Field(..., alias="rating") # e.g. "good" or "wrong"
    comment: Optional[str] = Field(default=None)

    model_config = ConfigDict(
        populate_by_name=True
    )

class FeedbackDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(..., alias="userId")
    question_id: str = Field(..., alias="questionId")
    predicted_topic: str = Field(..., alias="predictedTopic")
    correct_topic: str = Field(..., alias="correctTopic")
    rating: str
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class FeedbackResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str = Field(..., alias="userId")
    question_id: str = Field(..., alias="questionId")
    predicted_topic: str = Field(..., alias="predictedTopic")
    correct_topic: str = Field(..., alias="correctTopic")
    rating: str
    comment: Optional[str] = None
    created_at: datetime = Field(..., alias="createdAt")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
