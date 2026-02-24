import sys
import os

# Add the parent directory to the Python path to allow relative imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"[DEBUG] src/main.py - Project root: {project_root}")
print(f"[DEBUG] src/main.py - Python path: {sys.path[:3]}")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

# Import routes using relative imports
try:
    print("[DEBUG] Attempting to import api.routes.auth...")
    from src.api.routes import auth
    print("[DEBUG] Successfully imported auth routes")
except Exception as e:
    print(f"[DEBUG] Error importing auth routes: {e}")
    raise

try:
    print("[DEBUG] Attempting to import api.routes.todos...")
    from src.api.routes import todos
    print("[DEBUG] Successfully imported todos routes")
except Exception as e:
    print(f"[DEBUG] Error importing todos routes: {e}")
    raise

try:
    print("[DEBUG] Attempting to import api.routes.chatbot...")
    from src.api.routes import chatbot
    print("[DEBUG] Successfully imported chatbot routes")
except Exception as e:
    print(f"[DEBUG] Error importing chatbot routes: {e}")
    raise

try:
    print("[DEBUG] Attempting to import database...")
    from src.database.database import engine
    print("[DEBUG] Successfully imported database engine")
except Exception as e:
    print(f"[DEBUG] Error importing database: {e}")
    raise

try:
    print("[DEBUG] Attempting to import models...")
    from src.models.user import User
    from src.models.todo import Todo
    print("[DEBUG] Successfully imported models")
except Exception as e:
    print(f"[DEBUG] Error importing models: {e}")
    raise

app = FastAPI(title="Todo Management API", version="1.0.0")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(todos.router, prefix="/todos", tags=["todos"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])

@app.get("/")
def read_root():
    return {"message": "Todo Management API with AI Chatbot"}

@app.on_event("startup")
def on_startup():
    # Create database tables
    SQLModel.metadata.create_all(bind=engine)

from fastapi.responses import JSONResponse

# Error handling
@app.exception_handler(404)
async def not_found_error(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Resource not found"})

@app.exception_handler(500)
async def internal_error(request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# For testing purposes, we'll also add exception handlers for the specific errors we saw
@app.exception_handler(TypeError)
async def type_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": f"Type error: {str(exc)}"})
