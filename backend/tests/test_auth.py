import pytest
from httpx import AsyncClient

# Run all tests in this module inside the anyio event loop
pytestmark = pytest.mark.anyio

async def test_signup_successful(client: AsyncClient):
    payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "securepassword123"
    }
    response = await client.post("/api/auth/signup", json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}

async def test_signup_duplicate_email(client: AsyncClient):
    payload = {
        "name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "securepassword123"
    }
    # First sign up
    response1 = await client.post("/api/auth/signup", json=payload)
    assert response1.status_code == 201

    # Try duplicate sign up
    response2 = await client.post("/api/auth/signup", json=payload)
    assert response2.status_code == 400
    assert "Email already registered" in response2.json()["detail"]

async def test_signup_password_validation(client: AsyncClient):
    # Too short
    payload = {
        "name": "Short Pass User",
        "email": "shortpass@example.com",
        "password": "123"
    }
    response = await client.post("/api/auth/signup", json=payload)
    assert response.status_code == 422

    # Too long
    payload["password"] = "a" * 73
    response2 = await client.post("/api/auth/signup", json=payload)
    assert response2.status_code == 400
    assert "Password cannot exceed 72 characters" in response2.json()["detail"]

async def test_login_successful(client: AsyncClient):
    email = "loginuser@example.com"
    password = "correctpassword"
    
    # Signup
    await client.post("/api/auth/signup", json={
        "name": "Login User",
        "email": email,
        "password": password
    })

    # Login
    response = await client.post("/api/auth/login", data={
        "username": email,
        "password": password
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post("/api/auth/login", data={
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]
