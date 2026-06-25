import numpy as np
import logging
from typing import List, Dict, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity
from app.ai.embedding import generate_embedding
from app.ai.topics import TOPIC_DESCRIPTIONS

logger = logging.getLogger(__name__)

# Fallback precomputed topic embeddings for test/default cases
TOPIC_EMBEDDINGS = {}

def precompute_topic_embeddings():
    global TOPIC_EMBEDDINGS
    logger.info("Pre-computing fallback topic description embeddings...")
    try:
        for topic, desc in TOPIC_DESCRIPTIONS.items():
            emb = generate_embedding(desc)
            TOPIC_EMBEDDINGS[topic] = emb
    except Exception as e:
        logger.error(f"Error pre-computing fallback embeddings: {e}")

# Precompute on start
precompute_topic_embeddings()

def classify_topic(
    question_embedding: list[float], 
    db_topics: Optional[List[Dict]] = None
) -> Tuple[str, int]:
    """
    Classifies a question embedding into one of the topics in the db_topics list
    (or fallback predefined topics if db_topics is not provided) using cosine similarity.
    Returns a tuple of (topic_name, confidence_score).
    """
    if not db_topics:
        if not TOPIC_EMBEDDINGS:
            return "General", 0
            
        best_topic = "General"
        highest_similarity = -1.0
        question_vector = np.array(question_embedding).reshape(1, -1)
        
        for topic, emb in TOPIC_EMBEDDINGS.items():
            emb_vector = np.array(emb).reshape(1, -1)
            sim = cosine_similarity(question_vector, emb_vector)[0][0]
            if sim > highest_similarity:
                highest_similarity = sim
                best_topic = topic
                
        confidence = int(round(highest_similarity * 200))
        confidence = max(0, min(100, confidence))
        
        if confidence < 40:
            return "General", confidence
            
        return best_topic, confidence

    # Dynamic MongoDB topics classification
    best_topic = "General"
    highest_similarity = -1.0
    question_vector = np.array(question_embedding).reshape(1, -1)
    
    for t in db_topics:
        emb = t.get("embedding")
        if not emb:
            continue
        emb_vector = np.array(emb).reshape(1, -1)
        sim = cosine_similarity(question_vector, emb_vector)[0][0]
        if sim > highest_similarity:
            highest_similarity = sim
            best_topic = t["name"]
            
    confidence = int(round(highest_similarity * 200))
    confidence = max(0, min(100, confidence))
    
    # If the score is extremely low, return General or the closest match with low confidence
    if confidence < 40:
        return "General", confidence
        
    return best_topic, confidence
