import os
import pytest
from httpx import AsyncClient
from app.main import app
from app.database.mongodb import db, get_database

# Configure environment variables for testing
os.environ["JWT_SECRET"] = "test_jwt_secret_key_1234567890_test_only"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "15"

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture(autouse=True)
async def setup_test_db():
    from app.database.mongodb import connect_to_mongo, close_mongo_connection
    # Start database connection
    await connect_to_mongo()
    
    # Patch get_database in all modules importing it directly
    import app.database.mongodb as mongodb_mod
    import app.routes.auth as auth_route
    import app.routes.questions as questions_route
    import app.routes.deps as deps_route
    import services.ai_memory_service as memory_service
    import services.topic_learning_service as learning_service
    
    test_db_func = lambda: db.client["test_edtech_db"]
    
    original_mongodb_get_db = mongodb_mod.get_database
    original_auth_get_db = auth_route.get_database
    original_questions_get_db = questions_route.get_database
    original_deps_get_db = deps_route.get_database
    original_memory_get_db = memory_service.get_database
    original_learning_get_db = learning_service.get_database
    
    mongodb_mod.get_database = test_db_func
    auth_route.get_database = test_db_func
    questions_route.get_database = test_db_func
    deps_route.get_database = test_db_func
    memory_service.get_database = test_db_func
    learning_service.get_database = test_db_func
    
    # Clear collections before the test to ensure a clean state
    test_db = db.client["test_edtech_db"]
    await test_db["users"].drop()
    await test_db["questions"].drop()
    await test_db["topics"].drop()
    await test_db["discovered_topics"].drop()
    await test_db["feedback"].drop()
    await test_db["similarity_results"].drop()
    
    yield
    
    # Clean up test database collections after the test
    await test_db["users"].drop()
    await test_db["questions"].drop()
    await test_db["topics"].drop()
    await test_db["discovered_topics"].drop()
    await test_db["feedback"].drop()
    await test_db["similarity_results"].drop()
    
    # Restore functions and close connection
    mongodb_mod.get_database = original_mongodb_get_db
    auth_route.get_database = original_auth_get_db
    questions_route.get_database = original_questions_get_db
    deps_route.get_database = original_deps_get_db
    memory_service.get_database = original_memory_get_db
    learning_service.get_database = original_learning_get_db
    
    await close_mongo_connection()

@pytest.fixture
async def client():
    # Use ASGITransport if available (HTTPX >= 0.27.0), otherwise fall back to app parameter
    try:
        from httpx import ASGITransport
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
    except ImportError:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
