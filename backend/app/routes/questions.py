from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from bson import ObjectId

from app.models.user import UserDB
from app.database.mongodb import get_database
from app.routes.deps import get_current_user

# Models
from app.models.question_model import QuestionCreate, QuestionResponse, SimilarQuestion
from app.models.topic_model import TopicResponse, DiscoveredTopicResponse
from app.models.feedback_model import FeedbackCreate, FeedbackResponse

# Services
from services.ai_memory_service import save_question_memory, save_user_feedback
from services.topic_learning_service import approve_discovered_topic

router = APIRouter()
topics_router = APIRouter()
feedback_router = APIRouter()
discovered_topics_router = APIRouter()

# Fallback academic topics list for frontend compatibility in case MongoDB topics is empty
ACADEMIC_TOPICS = [
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Computer Science",
    "Software Engineering",
    "Web Development",
    "Database",
    "Cybersecurity",
    "Cloud Computing",
    "Quantum Computing",
    "Physics",
    "Chemistry",
    "Biology",
    "Mathematics",
    "History",
    "General"
]

@router.post("", response_model=QuestionResponse)
async def ask_question(question_in: QuestionCreate, current_user: UserDB = Depends(get_current_user)):
    """
    Submits a question, runs dynamic embedding, saves to AI memory, 
    calculates similarity against past questions, and triggers topic discovery if confidence is low.
    """
    model_name = question_in.model or "MiniLM Embedding Model"
    
    # Delegate core flow to AI Memory Service
    saved_doc = await save_question_memory(
        user_id=str(current_user.id),
        question_text=question_in.question,
        model_name=model_name
    )
    
    return {
        "_id": str(saved_doc["_id"]),
        "userId": saved_doc.get("userId") or saved_doc.get("user_id"),
        "question": saved_doc["question"],
        "topic": saved_doc["topic"],
        "confidence": saved_doc.get("confidence"),
        "similarQuestions": saved_doc.get("similarQuestions") or saved_doc.get("similar_questions") or [],
        "createdAt": saved_doc.get("createdAt") or saved_doc.get("created_at")
    }

@router.get("/history", response_model=List[QuestionResponse])
async def get_history(
    topic: Optional[str] = None, 
    current_user: UserDB = Depends(get_current_user)
):
    """
    Retrieves the current user's question history, with optional topic filtering.
    """
    db = get_database()
    user_id = str(current_user.id)
    
    query = {"$or": [{"userId": user_id}, {"user_id": user_id}]}
    
    if topic and topic.lower() != "all":
        query["topic"] = {"$regex": f"^{topic}$", "$options": "i"}
        
    cursor = db["questions"].find(query).sort("createdAt", -1)
    questions = await cursor.to_list(length=100)
    
    return [
        {
            "_id": str(q["_id"]),
            "userId": q.get("userId") or q.get("user_id"),
            "question": q["question"],
            "topic": q["topic"],
            "confidence": q.get("confidence"),
            "similarQuestions": q.get("similarQuestions") or q.get("similar_questions") or [],
            "createdAt": q.get("createdAt") or q.get("created_at")
        }
        for q in questions
    ]

@router.get("/dashboard-stats")
async def get_dashboard_stats(current_user: UserDB = Depends(get_current_user)):
    """
    Aggregates statistics for the user's dashboard.
    """
    db = get_database()
    user_id = str(current_user.id)
    
    query = {"$or": [{"userId": user_id}, {"user_id": user_id}]}
    total_questions = await db["questions"].count_documents(query)
    
    # Aggregate topic distribution for the user
    pipeline = [
        {"$match": query},
        {"$group": {"_id": "$topic", "count": {"$sum": 1}}}
    ]
    topic_distribution = []
    async for doc in db["questions"].aggregate(pipeline):
        topic_distribution.append({
            "topic": doc["_id"],
            "count": doc["count"]
        })
        
    # Fetch top 5 recent questions for dashboard preview
    cursor = db["questions"].find(query).sort("createdAt", -1).limit(5)
    recent_questions = await cursor.to_list(length=5)
    
    recent_mapped = [
        {
            "_id": str(q["_id"]),
            "userId": q.get("userId") or q.get("user_id"),
            "question": q["question"],
            "topic": q["topic"],
            "confidence": q.get("confidence"),
            "similarQuestions": q.get("similarQuestions") or q.get("similar_questions") or [],
            "createdAt": q.get("createdAt") or q.get("created_at")
        }
        for q in recent_questions
    ]
        
    return {
        "total_questions": total_questions,
        "topic_distribution": topic_distribution,
        "recent_questions": recent_mapped
    }

@router.get("/global-stats")
async def get_global_stats(current_user: UserDB = Depends(get_current_user)):
    """
    Retrieves global statistics across all users (accessible by admin only).
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin privilege required."
        )
    db = get_database()
    total_questions = await db["questions"].count_documents({})
    return {"total_questions": total_questions}

@router.get("/{id}", response_model=QuestionResponse)
async def get_question_by_id(id: str, current_user: UserDB = Depends(get_current_user)):
    """
    Retrieves a specific question by its ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question ID format"
        )
        
    db = get_database()
    question = await db["questions"].find_one({"_id": ObjectId(id)})
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
        
    db_user_id = question.get("userId") or question.get("user_id")
    if db_user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this question"
        )
        
    return {
        "_id": str(question["_id"]),
        "userId": db_user_id,
        "question": question["question"],
        "topic": question["topic"],
        "confidence": question.get("confidence"),
        "similarQuestions": question.get("similarQuestions") or question.get("similar_questions") or [],
        "createdAt": question.get("createdAt") or question.get("created_at")
    }

@topics_router.get("")
async def get_topics(format: Optional[str] = None):
    """
    Returns the list of active topics. Supports returning string array (default)
    or full Topic objects list if format='objects' is requested.
    """
    db = get_database()
    cursor = db["topics"].find({"status": "active"})
    db_topics = await cursor.to_list(length=100)
    
    if not db_topics:
        # Fallback to hardcoded list if database is empty/not seeded yet
        if format == "objects":
            return [
                {
                    "_id": "mock_id",
                    "name": t,
                    "description": "Fallback topic description",
                    "category": "Technology" if t in ACADEMIC_TOPICS[:11] else "Education",
                    "createdBy": "system",
                    "status": "active",
                    "createdAt": "2026-06-24T00:00:00"
                }
                for t in ACADEMIC_TOPICS
            ]
        return ACADEMIC_TOPICS
        
    if format == "objects":
        return [
            {
                "_id": str(t["_id"]),
                "name": t["name"],
                "description": t["description"],
                "category": t["category"],
                "createdBy": t.get("createdBy", "system"),
                "status": t["status"],
                "createdAt": t["createdAt"]
            }
            for t in db_topics
        ]
        
    return [t["name"] for t in db_topics]

@feedback_router.post("", response_model=FeedbackResponse)
async def submit_feedback(feedback_in: FeedbackCreate, current_user: UserDB = Depends(get_current_user)):
    """
    Submits user feedback about topic classification accuracy.
    """
    res = await save_user_feedback(user_id=str(current_user.id), feedback_in=feedback_in)
    return {
        "_id": str(res["_id"]),
        "userId": res["userId"],
        "questionId": res["questionId"],
        "predictedTopic": res["predictedTopic"],
        "correctTopic": res["correctTopic"],
        "rating": res["rating"],
        "comment": res.get("comment"),
        "createdAt": res["createdAt"]
    }

@discovered_topics_router.get("", response_model=List[DiscoveredTopicResponse])
async def get_discovered_topics(status_filter: str = "pending", current_user: UserDB = Depends(get_current_user)):
    """
    Retrieves the list of discovered topics filtered by status (pending, approved, rejected).
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privilege required to perform this action."
        )
        
    db = get_database()
    cursor = db["discovered_topics"].find({"status": status_filter})
    discovered = await cursor.to_list(length=100)
    
    return [
        {
            "_id": str(d["_id"]),
            "name": d["name"],
            "keywords": d.get("keywords", []),
            "questionCount": d.get("questionCount", 1),
            "status": d["status"],
            "createdAt": d["createdAt"]
        }
        for d in discovered
    ]

@discovered_topics_router.post("/{id}/approve", response_model=TopicResponse)
async def approve_topic(id: str, category: str = "Technology", current_user: UserDB = Depends(get_current_user)):
    """
    Admin action to approve a discovered topic and move it into the active topics collection.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privilege required to perform this action."
        )
        
    try:
        res = await approve_discovered_topic(id, category=category)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Discovered topic not found or already approved"
            )
        return {
            "_id": str(res["_id"]),
            "name": res["name"],
            "description": res["description"],
            "category": res["category"],
            "createdBy": res.get("createdBy", "admin"),
            "status": res["status"],
            "createdAt": res["createdAt"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@discovered_topics_router.post("/{id}/reject")
async def reject_topic(id: str, current_user: UserDB = Depends(get_current_user)):
    """
    Admin action to reject/dismiss a discovered topic candidate.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privilege required to perform this action."
        )
    try:
        db = get_database()
        res = await db["discovered_topics"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": "rejected"}}
        )
        if res.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Discovered topic not found or already processed"
            )
        return {"message": "Topic candidate successfully rejected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid ID or update failed: {str(e)}"
        )
