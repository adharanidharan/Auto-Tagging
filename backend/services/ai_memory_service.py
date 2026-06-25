import logging
from datetime import datetime
from bson import ObjectId
from typing import List, Dict, Optional

from app.database.mongodb import get_database
from app.ai.embedding import generate_embedding
from app.ai.classifier import classify_topic
from app.ai.similarity import find_similar_questions
from app.ai.topic_discovery import process_unknown_topic

from app.models.question_model import QuestionDB, QuestionResponse, SimilarQuestion, SimilarityResultDB, SimilarQuestionRef
from app.models.feedback_model import FeedbackDB, FeedbackResponse, FeedbackCreate

logger = logging.getLogger(__name__)

async def save_question_memory(user_id: str, question_text: str, model_name: str = "MiniLM Embedding Model") -> Dict:
    """
    Core AI memory flow:
    1. Generates embedding for the user's question.
    2. Classifies the topic dynamically using MongoDB 'topics'.
    3. Finds top similar questions in existing memory using cosine similarity.
    4. Handles low confidence classification by routing to discovered_topics.
    5. Saves the new question to the questions collection.
    6. Logs the query similarity details to similarity_results.
    """
    db = get_database()
    
    # 1. Generate local embedding
    embedding = generate_embedding(question_text, model_name=model_name)
    
    # 2. Fetch active topics from DB
    topics_cursor = db["topics"].find({"status": "active"})
    db_topics = await topics_cursor.to_list(length=100)
    
    # 3. Classify topic
    topic, confidence = classify_topic(embedding, db_topics)
    
    # Find matching topic ID from DB if it exists
    topic_id = None
    if db_topics:
        matched_t = next((t for t in db_topics if t["name"] == topic), None)
        if matched_t:
            topic_id = matched_t["_id"]
            
    # 4. Handle Low Confidence (< 50%) topic discovery
    if confidence < 50:
        logger.info(f"Low confidence ({confidence}%) for question: '{question_text}'. Triggering topic discovery...")
        cand = await process_unknown_topic(question_text, embedding, db["discovered_topics"])
        if cand:
            # If the candidate does not have an _id, it's a new discovery candidate that needs insertion
            if "_id" not in cand:
                await db["discovered_topics"].insert_one(cand)
            # We don't overwrite topic to General; we keep the predicted topic but flag it as low confidence

    # 5. Fetch past questions for semantic similarity search
    # Filter by the predicted topic first to guarantee contextual relevance
    questions_cursor = db["questions"].find({"topic": topic}).sort("createdAt", -1).limit(500)
    existing_questions = await questions_cursor.to_list(length=500)
    
    # Fallback to all questions if no questions exist under this topic
    if not existing_questions:
        questions_cursor = db["questions"].find({}).sort("createdAt", -1).limit(1000)
        existing_questions = await questions_cursor.to_list(length=1000)
        
    similar_matches = find_similar_questions(embedding, existing_questions, top_k=5)
    
    similar_questions_list = []
    similar_refs = []
    for item in similar_matches:
        similar_questions_list.append(
            SimilarQuestion(
                question=item["question"],
                topic=item["topic"],
                similarityScore=item["similarity_score"]
            )
        )
        if item.get("question_id"):
            similar_refs.append(
                SimilarQuestionRef(
                    questionId=item["question_id"],
                    score=item["similarity_score"]
                )
            )

    # 6. Save the new question to MongoDB (dynamic AI memory growth)
    question_doc = {
        "userId": user_id,
        "question": question_text,
        "answer": None,
        "embedding": embedding,
        "topicId": topic_id,
        "topic": topic,
        "confidence": confidence,
        "source": "user",
        "createdAt": datetime.utcnow(),
        "searchCount": 0,
        "similarQuestions": [s.model_dump(by_alias=True) for s in similar_questions_list]
    }
    
    insert_res = await db["questions"].insert_one(question_doc)
    question_id_str = str(insert_res.inserted_id)
    question_doc["_id"] = question_id_str
    
    # 7. Log to similarity_results for search history tracking & analytics
    if similar_refs:
        similarity_log = {
            "userId": user_id,
            "questionId": question_id_str,
            "similarQuestions": [s.model_dump(by_alias=True) for s in similar_refs],
            "createdAt": datetime.utcnow()
        }
        await db["similarity_results"].insert_one(similarity_log)
        
    return question_doc

async def save_user_feedback(user_id: str, feedback_in: FeedbackCreate) -> Dict:
    """
    Saves user feedback to the feedback collection to help improve classification.
    """
    db = get_database()
    feedback_doc = {
        "userId": user_id,
        "questionId": feedback_in.question_id,
        "predictedTopic": feedback_in.predicted_topic,
        "correctTopic": feedback_in.correct_topic,
        "rating": feedback_in.rating,
        "comment": feedback_in.comment,
        "createdAt": datetime.utcnow()
    }
    
    res = await db["feedback"].insert_one(feedback_doc)
    feedback_doc["_id"] = str(res.inserted_id)
    return feedback_doc
