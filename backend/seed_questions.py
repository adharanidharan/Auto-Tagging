import asyncio
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from app.database.mongodb import connect_to_mongo, get_database, close_mongo_connection
from app.ai.embedding import generate_embedding

SEED_DATA = {
    "Artificial Intelligence": [
        "What is AI?",
        "How does artificial intelligence work?",
        "What are intelligent systems?"
    ],
    "Deep Learning": [
        "What is neural network?",
        "Explain CNN",
        "What is transformer model?"
    ],
    "Machine Learning": [
        "What is supervised learning?",
        "What is regression?"
    ],
    "Programming": [
        "What is Python?",
        "What is JavaScript?"
    ],
    "Web Development": [
        "What is React?",
        "What is frontend?"
    ],
    "Database": [
        "What is MongoDB?",
        "What is SQL?"
    ]
}

async def seed():
    print("Connecting to MongoDB...")
    await connect_to_mongo()
    db = get_database()
    
    total_seeded = 0
    print("Seeding questions knowledge base...")
    for topic, questions in SEED_DATA.items():
        print(f"\nProcessing Topic: {topic}")
        for q_text in questions:
            # Check if duplicate exists
            exists = await db["questions"].find_one({"question": q_text})
            if exists:
                print(f"  - Skip (already exists): '{q_text}'")
                continue
                
            print(f"  - Generating embedding & inserting: '{q_text}'")
            embedding = generate_embedding(q_text)
            
            doc = {
                "userId": "system_seed",
                "question": q_text,
                "topic": topic,
                "confidence": 100,  # Seeded questions are 100% confidence
                "embedding": embedding,
                "similarQuestions": [],
                "createdAt": datetime.utcnow()
            }
            await db["questions"].insert_one(doc)
            total_seeded += 1
            
    print(f"\nSuccessfully seeded {total_seeded} questions into database!")
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(seed())
