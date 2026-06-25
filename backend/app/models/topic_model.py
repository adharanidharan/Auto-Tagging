from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from app.models.question_model import PyObjectId

class TopicDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    embedding: List[float]
    category: str = Field(default="Technology")
    created_by: str = Field(default="system", alias="createdBy")
    status: str = Field(default="active")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class TopicResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str
    category: str
    created_by: str = Field(alias="createdBy")
    status: str
    created_at: datetime = Field(alias="createdAt")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class DiscoveredTopicDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    keywords: List[str]
    question_count: int = Field(default=1, alias="questionCount")
    embedding: List[float]
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class DiscoveredTopicResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    keywords: List[str]
    question_count: int = Field(alias="questionCount")
    status: str
    created_at: datetime = Field(alias="createdAt")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
