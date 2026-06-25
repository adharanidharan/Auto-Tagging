import asyncio
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from app.database.mongodb import connect_to_mongo, get_database, close_mongo_connection
from app.ai.embedding import generate_embedding

SEED_QUESTIONS = [
    # Biology
    {"question": "Explain the light-dependent and light-independent reactions of photosynthesis.", "topic": "Biology"},
    {"question": "What is the structure and function of the mitochondria in eukaryotic cells?", "topic": "Biology"},
    {"question": "How does DNA replication occur and what enzymes are involved?", "topic": "Biology"},
    {"question": "Describe the process of mitosis and meiosis in cell division.", "topic": "Biology"},
    {"question": "What is natural selection and how does it drive evolution?", "topic": "Biology"},
    # Physics
    {"question": "What are Newton's three laws of motion and how do they apply to daily life?", "topic": "Physics"},
    {"question": "State the law of universal gravitation and explain how gravity works.", "topic": "Physics"},
    {"question": "What is the difference between kinetic energy and potential energy?", "topic": "Physics"},
    {"question": "Explain the theory of special relativity and time dilation.", "topic": "Physics"},
    {"question": "How do electromagnetic waves propagate and what is the speed of light?", "topic": "Physics"},
    # Mathematics
    {"question": "How do you solve a system of linear equations using matrix inversion?", "topic": "Mathematics"},
    {"question": "Explain the fundamental theorem of calculus and how derivatives relate to integrals.", "topic": "Mathematics"},
    {"question": "What is the Pythagorean theorem and how is it used in trigonometry?", "topic": "Mathematics"},
    {"question": "Define probability distributions and explain the difference between discrete and continuous variables.", "topic": "Mathematics"},
    {"question": "What is a vector space and what are the axioms of linear algebra?", "topic": "Mathematics"},
    # Computer Science
    {"question": "Compare the time complexity of Quick Sort, Merge Sort, and Bubble Sort algorithms.", "topic": "Computer Science"},
    {"question": "What is the difference between a stack, a queue, and a linked list?", "topic": "Computer Science"},
    {"question": "Explain the MVC (Model-View-Controller) design pattern in software engineering.", "topic": "Computer Science"},
    {"question": "What is a neural network and how does backpropagation work in machine learning?", "topic": "Computer Science"},
    {"question": "How does a relational database (SQL) differ from a non-relational database (NoSQL) like MongoDB?", "topic": "Computer Science"},
    # Chemistry
    {"question": "Explain the difference between ionic bonding, covalent bonding, and metallic bonding.", "topic": "Chemistry"},
    {"question": "How is the periodic table organized and what are periodic trends?", "topic": "Chemistry"},
    {"question": "What are organic compounds and what defines functional groups in organic chemistry?", "topic": "Chemistry"},
    {"question": "Define pH and explain the difference between strong acids and weak bases.", "topic": "Chemistry"},
    {"question": "How do you balance a chemical equation and calculate stoichiometry?", "topic": "Chemistry"},
    # History
    {"question": "What were the primary causes and consequences of the French Revolution?", "topic": "History"},
    {"question": "Explain the significance of the Magna Carta in the history of constitutional law.", "topic": "History"},
    {"question": "Describe the rise and fall of the Roman Empire and its legacy.", "topic": "History"},
    {"question": "What were the main factors that led to the outbreak of World War I?", "topic": "History"},
    {"question": "Who was Mahatma Gandhi and what was his role in the Indian Independence Movement?", "topic": "History"},
]

async def seed():
    print("Connecting to MongoDB...")
    await connect_to_mongo()
    db = get_database()
    
    print(f"Generating embeddings and seeding {len(SEED_QUESTIONS)} questions...")
    for idx, item in enumerate(SEED_QUESTIONS, start=1):
        question_text = item["question"]
        topic = item["topic"]
        
        # Check if already exists to avoid duplicates
        exists = await db["questions"].find_one({"question": question_text})
        if exists:
            print(f"[{idx}/{len(SEED_QUESTIONS)}] Skip (already exists): {question_text[:50]}...")
            continue
            
        print(f"[{idx}/{len(SEED_QUESTIONS)}] Processing: {question_text[:50]}...")
        embedding = generate_embedding(question_text)
        
        doc = {
            "userId": "system_seed",
            "question": question_text,
            "topic": topic,
            "embedding": embedding,
            "similarQuestions": [],
            "createdAt": datetime.utcnow()
        }
        await db["questions"].insert_one(doc)
        
    print("\nDatabase seeded successfully!")
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(seed())
