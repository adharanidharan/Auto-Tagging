from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, *args, **kwargs):
        field_schema.update(type="string")

class QuestionCreate(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)
    model: Optional[str] = Field("MiniLM Embedding Model", alias="model")

class SimilarQuestion(BaseModel):
    question: str
    topic: str
    similarity_score: float = Field(..., alias="similarityScore")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class QuestionDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(..., alias="userId")
    question: str
    answer: Optional[str] = Field(default=None, alias="answer")
    embedding: List[float]
    topic_id: Optional[PyObjectId] = Field(default=None, alias="topicId")
    topic: str
    confidence: Optional[int] = None
    source: str = Field(default="user", alias="source")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    search_count: int = Field(default=0, alias="searchCount")
    similar_questions: List[SimilarQuestion] = Field(default=[], alias="similarQuestions")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class QuestionResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str = Field(..., alias="userId")
    question: str
    answer: Optional[str] = Field(default=None, alias="answer")
    topic: str
    confidence: Optional[int] = None
    source: str = Field(default="user", alias="source")
    similar_questions: List[SimilarQuestion] = Field(default=[], alias="similarQuestions")
    created_at: datetime = Field(..., alias="createdAt")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class SimilarQuestionRef(BaseModel):
    question_id: str = Field(..., alias="questionId")
    score: float

class SimilarityResultDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(..., alias="userId")
    question_id: str = Field(..., alias="questionId")
    similar_questions: List[SimilarQuestionRef] = Field(..., alias="similarQuestions")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
