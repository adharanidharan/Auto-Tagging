import logging
from datetime import datetime
from bson import ObjectId
from typing import List, Dict, Optional

from app.database.mongodb import get_database
from app.ai.embedding import generate_embedding
from app.models.topic_model import TopicDB, DiscoveredTopicDB

logger = logging.getLogger(__name__)

INITIAL_TOPICS = [
    # Category: Technology
    {"name": "Artificial Intelligence", "description": "AI machine intelligence neural networks deep learning", "category": "Technology"},
    {"name": "Machine Learning", "description": "machine learning ML training models prediction classification regression algorithms", "category": "Technology"},
    {"name": "Deep Learning", "description": "deep learning neural networks CNN RNN transformers backpropagation", "category": "Technology"},
    {"name": "Data Science", "description": "data analysis statistics visualization pandas numpy datasets", "category": "Technology"},
    {"name": "Computer Science", "description": "computer science algorithms operating systems data structures theory computation", "category": "Technology"},
    {"name": "Software Engineering", "description": "software engineering clean code architecture design patterns testing git developer refactoring", "category": "Technology"},
    {"name": "Web Development", "description": "frontend backend react html css javascript web application node express", "category": "Technology"},
    {"name": "Database", "description": "SQL MongoDB database queries data storage schema postgres indexing reltional nosql", "category": "Technology"},
    {"name": "Cybersecurity", "description": "security encryption hacking authentication firewall protection malware threat vulnerability", "category": "Technology"},
    {"name": "Cloud Computing", "description": "AWS Azure cloud servers deployment infrastructure docker kubernetes scaling hosting", "category": "Technology"},
    {"name": "Quantum Computing", "description": "quantum computing qubits physics quantum algorithms superposition entanglement computer", "category": "Technology"},
    
    # Category: Education
    {"name": "Physics", "description": "force energy motion gravity laws physics dynamics thermodynamics kinematics light relativity", "category": "Education"},
    {"name": "Chemistry", "description": "elements reactions molecules chemistry organic inorganic bonding periodic table equations", "category": "Education"},
    {"name": "Biology", "description": "cells plants genetics human body biology ecology evolution organisms photosynthesis anatomy", "category": "Education"},
    {"name": "Mathematics", "description": "numbers equations algebra calculus mathematics geometry statistics trigonometry math", "category": "Education"},
    {"name": "History", "description": "events civilization war historical information ancient modern empire revolution world", "category": "Education"}
]

async def initialize_topics():
    """
    Checks if the topics collection is empty in MongoDB.
    If empty, precomputes embeddings for the 16 initial academic/tech topics and inserts them.
    This runs on application startup.
    """
    db = get_database()
    
    # Check if there are any active topics
    count = await db["topics"].count_documents({"status": "active"})
    if count > 0:
        logger.info(f"Database already populated with {count} active topics. Skipping seeding.")
        return
        
    logger.info("Topics collection is empty. Seeding initial 16 subjects/technologies...")
    
    seeded_docs = []
    for topic_info in INITIAL_TOPICS:
        try:
            # Generate embedding for the description
            embedding = generate_embedding(topic_info["description"])
            
            topic_doc = {
                "name": topic_info["name"],
                "description": topic_info["description"],
                "embedding": embedding,
                "category": topic_info["category"],
                "createdBy": "system",
                "status": "active",
                "createdAt": datetime.utcnow()
            }
            seeded_docs.append(topic_doc)
        except Exception as e:
            logger.error(f"Failed to generate embedding/seed topic '{topic_info['name']}': {e}")
            
    if seeded_docs:
        await db["topics"].insert_many(seeded_docs)
        logger.info(f"Successfully seeded {len(seeded_docs)} topics into MongoDB.")

async def approve_discovered_topic(discovered_topic_id: str, category: str = "Technology") -> Optional[Dict]:
    """
    Admin approval flow:
    1. Fetches a discovered topic by ID.
    2. Changes its status to "approved".
    3. Moves/promotes it into the topics collection as an active topic.
    """
    db = get_database()
    
    if not ObjectId.is_valid(discovered_topic_id):
        raise ValueError("Invalid Discovered Topic ID")
        
    obj_id = ObjectId(discovered_topic_id)
    
    # 1. Fetch discovered topic
    discovered = await db["discovered_topics"].find_one({"_id": obj_id})
    if not discovered:
        logger.warning(f"Discovered topic {discovered_topic_id} not found.")
        return None
        
    if discovered.get("status") != "pending":
        logger.warning(f"Discovered topic {discovered_topic_id} is already '{discovered.get('status')}'.")
        return None
        
    # 2. Promote to active topics collection
    # Generate description from keywords
    keywords_list = discovered.get("keywords", [])
    description = f"Dynamic topic {discovered['name']} containing keywords: " + " ".join(keywords_list)
    
    topic_doc = {
        "name": discovered["name"],
        "description": description,
        "embedding": discovered["embedding"],
        "category": category,
        "createdBy": "admin",
        "status": "active",
        "createdAt": datetime.utcnow()
    }
    
    await db["topics"].insert_one(topic_doc)
    
    # 3. Update status in discovered_topics to "approved"
    await db["discovered_topics"].update_one(
        {"_id": obj_id},
        {"$set": {"status": "approved"}}
    )
    
    topic_doc["_id"] = str(topic_doc["_id"])
    return topic_doc
