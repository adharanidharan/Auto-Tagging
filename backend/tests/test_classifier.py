import pytest
from app.ai.embedding import generate_embedding
from app.ai.classifier import classify_topic

# Run all tests in this module inside the anyio event loop
pytestmark = pytest.mark.anyio

async def test_generate_embedding():
    text = "What is the capital of France?"
    emb = generate_embedding(text)
    assert isinstance(emb, list)
    assert len(emb) == 384
    assert all(isinstance(val, float) for val in emb)

async def test_classify_topic_ai():
    text = "What is AI?"
    emb = generate_embedding(text)
    topic, confidence = classify_topic(emb)
    assert topic == "Artificial Intelligence"
    assert confidence >= 40

async def test_classify_topic_neural_network():
    text = "Explain neural network"
    emb = generate_embedding(text)
    topic, confidence = classify_topic(emb)
    assert topic == "Deep Learning"
    assert confidence >= 40

async def test_classify_topic_react():
    text = "What is React?"
    emb = generate_embedding(text)
    topic, confidence = classify_topic(emb)
    assert topic == "Web Development"
    assert confidence >= 40

async def test_classify_topic_photosynthesis():
    text = "What is photosynthesis?"
    emb = generate_embedding(text)
    topic, confidence = classify_topic(emb)
    assert topic == "Biology"
    assert confidence >= 40

async def test_classify_topic_gravity():
    text = "What is gravity?"
    emb = generate_embedding(text)
    topic, confidence = classify_topic(emb)
    assert topic == "Physics"
    assert confidence >= 40

async def test_classify_topic_general_fallback():
    text = "hello world how are you today"
    emb = generate_embedding(text)
    topic, confidence = classify_topic(emb)
    # Very low cosine similarity, should fall back to General
    assert topic == "General"
    assert confidence < 40
