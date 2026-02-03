import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.database import engine
from sqlmodel import SQLModel, Session
from src.models.user import User
from unittest.mock import patch

client = TestClient(app)

def test_register_user():
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert "id" in data

def test_register_duplicate_email():
    """Test registration with duplicate email"""
    # First registration should succeed
    client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
    )

    # Second registration with same email should fail
    response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "anotherpassword123",
            "password_confirm": "anotherpassword123",
            "first_name": "Another",
            "last_name": "User"
        }
    )
    assert response.status_code == 409

def test_login_valid_credentials():
    """Test login with valid credentials"""
    # First register a user
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
            "first_name": "Login",
            "last_name": "Test"
        }
    )

    # Then try to login
    response = client.post(
        "/auth/login",
        data={
            "email": "login@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data

def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/auth/login",
        data={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 400

def test_logout():
    """Test logout endpoint"""
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"