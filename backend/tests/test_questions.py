import pytest
from httpx import AsyncClient

# Run all tests in this module inside the anyio event loop
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

async def test_ask_question(client: AsyncClient):
    headers = await get_auth_headers(client, "asker@example.com")
    
    # 1. Ask first question
    payload = {
        "question": "What is the definition of photosynthesis and chlorophyll?",
        "model": "MiniLM Embedding Model"
    }
    response = await client.post("/api/questions", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == payload["question"]
    assert data["topic"] == "Biology"
    assert "similarQuestions" in data
    assert len(data["similarQuestions"]) == 0

    # 2. Ask a highly similar second question to verify similarity matching
    payload_similar = {
        "question": "Explain how photosynthesis works in plants",
        "model": "MiniLM Embedding Model"
    }
    response_sim = await client.post("/api/questions", json=payload_similar, headers=headers)
    assert response_sim.status_code == 200
    data_sim = response_sim.json()
    assert data_sim["topic"] == "Biology"
    assert len(data_sim["similarQuestions"]) > 0
    # The first question should be returned as similar
    assert data_sim["similarQuestions"][0]["question"] == payload["question"]
    assert data_sim["similarQuestions"][0]["topic"] == "Biology"
    assert data_sim["similarQuestions"][0]["similarityScore"] > 0.5

async def test_get_history_and_filters(client: AsyncClient):
    headers = await get_auth_headers(client, "history@example.com")
    
    # Post a Biology question
    await client.post("/api/questions", json={
        "question": "What is the cell membrane function in animal cell?",
        "model": "MiniLM Embedding Model"
    }, headers=headers)
    
    # Post a Physics question
    await client.post("/api/questions", json={
        "question": "Calculate the gravitational force between earth and moon",
        "model": "MiniLM Embedding Model"
    }, headers=headers)

    # Get history (All)
    response = await client.get("/api/questions/history", headers=headers)
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 2

    # Get history filtered by Biology
    response_bio = await client.get("/api/questions/history?topic=Biology", headers=headers)
    assert response_bio.status_code == 200
    bio_history = response_bio.json()
    assert len(bio_history) == 1
    assert bio_history[0]["topic"] == "Biology"

    # Get history filtered by Physics
    response_phys = await client.get("/api/questions/history?topic=Physics", headers=headers)
    assert response_phys.status_code == 200
    phys_history = response_phys.json()
    assert len(phys_history) == 1
    assert phys_history[0]["topic"] == "Physics"

async def test_dashboard_stats(client: AsyncClient):
    headers = await get_auth_headers(client, "stats@example.com")
    
    # Post 2 questions
    await client.post("/api/questions", json={
        "question": "Explain chemical bonding and covalent bonds",
        "model": "MiniLM Embedding Model"
    }, headers=headers)
    
    await client.post("/api/questions", json={
        "question": "What is the periodic table of elements?",
        "model": "MiniLM Embedding Model"
    }, headers=headers)

    response = await client.get("/api/questions/dashboard-stats", headers=headers)
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_questions"] == 2
    assert len(stats["topic_distribution"]) == 1
    assert stats["topic_distribution"][0]["topic"] == "Chemistry"
    assert stats["topic_distribution"][0]["count"] == 2
    assert len(stats["recent_questions"]) == 2

async def test_get_question_by_id(client: AsyncClient):
    headers = await get_auth_headers(client, "qbyid@example.com")
    
    # Create question
    payload = {
        "question": "Explain the significance of the Magna Carta in world history",
        "model": "MiniLM Embedding Model"
    }
    response = await client.post("/api/questions", json=payload, headers=headers)
    q_id = response.json()["_id"]

    # Fetch by ID
    get_response = await client.get(f"/api/questions/{q_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["question"] == payload["question"]
    assert get_response.json()["topic"] == "History"

    # Fetch by invalid ID
    bad_response = await client.get("/api/questions/invalidid123", headers=headers)
    assert bad_response.status_code == 400
    
    # Fetch by non-existent ID
    from bson import ObjectId
    fake_id = str(ObjectId())
    fake_response = await client.get(f"/api/questions/{fake_id}", headers=headers)
    assert fake_response.status_code == 404
