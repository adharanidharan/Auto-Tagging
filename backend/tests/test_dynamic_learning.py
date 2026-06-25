import pytest
from datetime import datetime
from httpx import AsyncClient
from bson import ObjectId
import app.database.mongodb as mongodb
from services.topic_learning_service import initialize_topics

pytestmark = pytest.mark.anyio

async def get_auth_headers(client: AsyncClient, email: str, name: str = "Test User") -> dict:
    password = "password123"
    await client.post("/api/auth/signup", json={
        "name": name,
        "email": email,
        "password": password
    })
    response = await client.post("/api/auth/login", data={
        "username": email,
        "password": password
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

async def test_topic_seeding_and_retrieval(client: AsyncClient):
    headers = await get_auth_headers(client, "seeder@example.com")
    
    # 1. Seeding should have been run in startup/fixture but let's run it explicitly on our test DB
    await initialize_topics()
    
    # 2. Retrieve topics in standard string format
    response = await client.get("/api/topics", headers=headers)
    assert response.status_code == 200
    topics_list = response.json()
    assert "Artificial Intelligence" in topics_list
    assert "Physics" in topics_list
    assert "General" not in topics_list # General is not in the seeded list (it's a fallback)

    # 3. Retrieve topics in full object format
    response_obj = await client.get("/api/topics?format=objects", headers=headers)
    assert response_obj.status_code == 200
    topics_objects = response_obj.json()
    assert len(topics_objects) > 0
    assert topics_objects[0]["name"] == "Artificial Intelligence"
    assert topics_objects[0]["status"] == "active"

async def test_low_confidence_topic_discovery_flow(client: AsyncClient):
    headers = await get_auth_headers(client, "discovery@example.com")
    db = mongodb.get_database()
    
    # Pre-seed topics so we have an active vocabulary
    await initialize_topics()

    # 1. Ask a question with low confidence (gibberish/unrelated) to guarantee < 50% confidence
    payload = {
        "question": "gibberish qwerty random input query",
        "model": "MiniLM Embedding Model"
    }
    
    response = await client.post("/api/questions", json=payload, headers=headers)
    assert response.status_code == 200
    
    # Check that a pending discovered topic has been created in DB
    cursor = db["discovered_topics"].find({"status": "pending"})
    discovered = await cursor.to_list(length=10)
    assert len(discovered) == 1
    
    candidate = discovered[0]
    assert "gibberish" in candidate["keywords"] or "qwerty" in candidate["keywords"]
    assert candidate["questionCount"] == 1

    # 2. Ask a highly similar low-confidence question to trigger online clustering/merging
    payload_similar = {
        "question": "gibberish qwerty random input search",
        "model": "MiniLM Embedding Model"
    }
    response_sim = await client.post("/api/questions", json=payload_similar, headers=headers)
    assert response_sim.status_code == 200
    
    # Check that it did not create a new candidate, but rather merged into the existing one
    discovered_after = await db["discovered_topics"].find({"status": "pending"}).to_list(length=10)
    assert len(discovered_after) == 1
    assert discovered_after[0]["questionCount"] == 2
    assert "search" in discovered_after[0]["keywords"] or "qwerty" in discovered_after[0]["keywords"]

async def test_discovered_topic_approval_flow(client: AsyncClient):
    headers = await get_auth_headers(client, "admin@example.com")
    db = mongodb.get_database()
    
    # Seed active topics
    await initialize_topics()
    
    # Create a mock pending discovered topic directly
    mock_discovered = {
        "name": "Quantum Machine Learning",
        "keywords": ["quantum", "machine", "learning"],
        "questionCount": 3,
        "embedding": [0.1] * 384,
        "status": "pending",
        "createdAt": datetime.utcnow()
    }
    res = await db["discovered_topics"].insert_one(mock_discovered)
    discovered_id = str(res.inserted_id)
    
    # Get pending discovered topics via endpoint
    response_list = await client.get("/api/discovered-topics?status_filter=pending", headers=headers)
    assert response_list.status_code == 200
    pending_list = response_list.json()
    assert len(pending_list) == 1
    assert pending_list[0]["name"] == "Quantum Machine Learning"
    
    # Approve the discovered topic
    response_approve = await client.post(
        f"/api/discovered-topics/{discovered_id}/approve?category=Technology",
        headers=headers
    )
    assert response_approve.status_code == 200
    approved_data = response_approve.json()
    assert approved_data["name"] == "Quantum Machine Learning"
    assert approved_data["status"] == "active"
    
    # Check that status is updated in discovered_topics collection
    updated_disc = await db["discovered_topics"].find_one({"_id": ObjectId(discovered_id)})
    assert updated_disc["status"] == "approved"
    
    # Check that it is now active in topics collection
    active_topic = await db["topics"].find_one({"name": "Quantum Machine Learning", "status": "active"})
    assert active_topic is not None
    assert active_topic["category"] == "Technology"

async def test_feedback_submission(client: AsyncClient):
    headers = await get_auth_headers(client, "feedback_user@example.com")
    db = mongodb.get_database()
    
    # Ask a question to get a question ID
    await initialize_topics()
    payload = {
        "question": "Explain deep learning convolutional networks",
        "model": "MiniLM Embedding Model"
    }
    response = await client.post("/api/questions", json=payload, headers=headers)
    assert response.status_code == 200
    question_id = response.json()["_id"]
    
    # Submit feedback
    feedback_payload = {
        "questionId": question_id,
        "predictedTopic": "General",
        "correctTopic": "Deep Learning",
        "rating": "wrong",
        "comment": "It predicted general but should be Deep Learning"
    }
    
    feedback_res = await client.post("/api/feedback", json=feedback_payload, headers=headers)
    assert feedback_res.status_code == 200
    data = feedback_res.json()
    assert data["predictedTopic"] == "General"
    assert data["correctTopic"] == "Deep Learning"
    assert data["rating"] == "wrong"
    
    # Check DB persistence
    saved_feedback = await db["feedback"].find_one({"questionId": question_id})
    assert saved_feedback is not None
    assert saved_feedback["rating"] == "wrong"
