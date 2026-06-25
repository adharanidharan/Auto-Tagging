import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_questions(new_embedding: list[float], existing_questions: list[dict], top_k: int = 5) -> list[dict]:
    """
    Finds the top_k most semantically similar questions using cosine similarity.
    Calculates similarity between the new question's embedding and all historical question embeddings.
    """
    if not existing_questions:
        return []

    # Extract embeddings (handling potential camelCase/snake_case representation from DB)
    embeddings = []
    valid_questions = []
    
    for q in existing_questions:
        # Check both embedding keys just in case
        emb = q.get("embedding")
        if emb and isinstance(emb, list) and len(emb) == len(new_embedding):
            embeddings.append(emb)
            valid_questions.append(q)
            
    if not embeddings:
        return []

    # Calculate cosine similarity
    similarities = cosine_similarity([new_embedding], embeddings)[0]
    
    # Combine questions with their similarity scores
    scored_questions = []
    for i, q in enumerate(valid_questions):
        scored_questions.append({
            "question_id": str(q.get("_id") or q.get("id") or ""),
            "question": q["question"],
            "topic": q["topic"],
            "similarity_score": float(similarities[i])
        })
    
    # Sort by similarity score descending
    scored_questions.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    # Return top_k matches
    return scored_questions[:top_k]
