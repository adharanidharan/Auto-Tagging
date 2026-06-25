import os
import sys
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Ensure the root of the project is in the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from app.database.mongodb import connect_to_mongo, get_database, close_mongo_connection
from sentence_transformers import SentenceTransformer

async def seed():
    print("Loading dataset...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(script_dir)
    dataset_path = os.path.join(backend_dir, "datasets", "education_technology_questions.json")
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file not found at {dataset_path}")
        return
        
    with open(dataset_path, "r") as f:
        dataset = json.load(f)
        
    print(f"Loaded {len(dataset)} questions from JSON.")
    
    # Connect to MongoDB
    await connect_to_mongo()
    db = get_database()
    
    # Create indexes for faster queries as requested
    print("Creating database indexes...")
    await db["questions"].create_index("question")
    await db["questions"].create_index("topic")
    await db["questions"].create_index("category")
    await db["questions"].create_index("createdAt")
    
    # Duplicate checking: Fetch all existing question texts from the database
    print("Fetching existing questions for duplicate checking...")
    cursor = db["questions"].find({}, {"question": 1})
    existing_questions = {doc["question"] for doc in await cursor.to_list(length=None)}
    print(f"Found {len(existing_questions)} existing questions in the database.")
    
    # Filter out duplicates
    new_items = [item for item in dataset if item["question"] not in existing_questions]
    skipped_count = len(dataset) - len(new_items)
    print(f"Skipping {skipped_count} duplicate questions.")
    
    if not new_items:
        print("No new questions to insert. Database is already up to date.")
        await close_mongo_connection()
        return

    print("Generating embeddings...")
    # Load SentenceTransformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Batch encode questions
    questions_text = [item["question"] for item in new_items]
    print(f"Generating embeddings for {len(questions_text)} questions in batch mode...")
    embeddings = model.encode(questions_text, show_progress_bar=True)
    
    print("Preparing documents for insert...")
    docs_to_insert = []
    for item, embedding in zip(new_items, embeddings):
        doc = {
            "question": item["question"],
            "answer": item["answer"],
            "topic": item["topic"],
            "subtopic": item["subtopic"],
            "category": item["category"],
            "difficulty": item["difficulty"],
            "embedding": embedding.tolist(),
            "source": "dataset",
            "searchCount": 0,
            "createdAt": datetime.utcnow()
        }
        docs_to_insert.append(doc)
        
    print(f"Inserting {len(docs_to_insert)} questions...")
    # Insert in batches of 1000 to keep the payload size safe
    batch_size = 1000
    inserted_count = 0
    for i in range(0, len(docs_to_insert), batch_size):
        batch = docs_to_insert[i:i + batch_size]
        await db["questions"].insert_many(batch)
        inserted_count += len(batch)
        print(f"Inserted: {inserted_count} questions")
        
    print("Dataset import completed.")
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(seed())
