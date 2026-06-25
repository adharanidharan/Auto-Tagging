from datetime import datetime
import re
import numpy as np
from typing import List, Dict, Optional
from sklearn.metrics.pairwise import cosine_similarity

STOP_WORDS = {
    "what", "is", "a", "an", "the", "how", "to", "why", "of", "in", "on", "at", 
    "for", "with", "about", "against", "between", "into", "through", "during", 
    "before", "after", "above", "below", "from", "up", "down", "out", "off", 
    "over", "under", "again", "further", "then", "once", "here", "there", 
    "when", "where", "all", "any", "both", "each", "few", "more", "most", 
    "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", 
    "than", "too", "very", "can", "will", "just", "should", "now", "explain", 
    "describe", "define", "question", "ask", "tell", "show", "give", "please",
    "get", "find", "search", "lookup"
}

def extract_keywords(text: str) -> List[str]:
    """
    Cleans text, removes stop words, and returns a list of unique keywords.
    """
    # Remove punctuation and special characters
    clean_text = re.sub(r"[^\w\s-]", "", text.lower())
    words = clean_text.split()
    
    keywords = []
    for word in words:
        # Keep words that are not stop words and are longer than 2 characters
        if word not in STOP_WORDS and len(word) > 2 and not word.isdigit():
            keywords.append(word)
            
    # Return unique keywords while preserving order
    seen = set()
    return [k for k in keywords if not (k in seen or seen.add(k))]

def generate_candidate_name(question: str, keywords: List[str]) -> str:
    """
    Generates a capitalized candidate topic name from the question and keywords.
    """
    if not keywords:
        return "Unknown Concept"
        
    # Take up to 3 descriptive keywords
    name_words = keywords[:3]
    return " ".join(word.capitalize() for word in name_words)

async def process_unknown_topic(
    question_text: str,
    question_embedding: List[float],
    discovered_topics_col
) -> Optional[Dict]:
    """
    Processes a low confidence question by either merging it into an existing 
    discovered_topic or creating a new candidate topic.
    """
    # 1. Fetch all pending discovered topics
    cursor = discovered_topics_col.find({"status": "pending"})
    pending_candidates = await cursor.to_list(length=100)
    
    best_candidate = None
    highest_similarity = -1.0
    
    # Reshape current embedding for sklearn comparison
    question_vector = np.array(question_embedding).reshape(1, -1)
    
    for cand in pending_candidates:
        emb = cand.get("embedding")
        if not emb:
            continue
        emb_vector = np.array(emb).reshape(1, -1)
        sim = cosine_similarity(question_vector, emb_vector)[0][0]
        
        if sim > highest_similarity:
            highest_similarity = sim
            best_candidate = cand
            
    # 2. Extract keywords from current question
    new_keywords = extract_keywords(question_text)
    
    # 3. Determine if we merge or create
    # A similarity of >= 0.65 suggests the questions belong to the same topic domain
    if highest_similarity >= 0.65 and best_candidate:
        # Update existing candidate (Online Clustering / Aggregation)
        old_count = best_candidate.get("questionCount", 1)
        new_count = old_count + 1
        
        # Calculate running average embedding
        old_emb = np.array(best_candidate["embedding"])
        new_emb = (old_emb * old_count + np.array(question_embedding)) / new_count
        
        # Merge keywords
        merged_keywords = list(set(best_candidate.get("keywords", []) + new_keywords))
        
        # Perform DB Update
        await discovered_topics_col.update_one(
            {"_id": best_candidate["_id"]},
            {
                "$set": {
                    "questionCount": new_count,
                    "embedding": new_emb.tolist(),
                    "keywords": merged_keywords
                }
            }
        )
        
        # Return updated record representation
        best_candidate["questionCount"] = new_count
        best_candidate["keywords"] = merged_keywords
        return best_candidate
    else:
        # Create a new pending topic candidate
        candidate_name = generate_candidate_name(question_text, new_keywords)
        
        new_candidate = {
            "name": candidate_name,
            "keywords": new_keywords,
            "questionCount": 1,
            "embedding": question_embedding,
            "status": "pending",
            "createdAt": datetime.utcnow()
        }
        return new_candidate
