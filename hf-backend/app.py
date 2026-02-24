"""
Todo Management API - Hugging Face Spaces Standalone Version
This is a self-contained version that works on HF Spaces
Includes AI Chatbot feature with Gemini API integration
"""
import os
import sys
import uuid
import jwt
import json
import google.generativeai as genai
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

# FastAPI and SQLModel imports
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

# ============= Configuration =============
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Clean up DATABASE_URL - remove any 'psql ' prefix or quotes
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
if DATABASE_URL.startswith("psql "):
    DATABASE_URL = DATABASE_URL[5:]  # Remove 'psql ' prefix
if DATABASE_URL.startswith("'") and DATABASE_URL.endswith("'"):
    DATABASE_URL = DATABASE_URL[1:-1]  # Remove surrounding quotes
if DATABASE_URL.startswith('"') and DATABASE_URL.endswith('"'):
    DATABASE_URL = DATABASE_URL[1:-1]  # Remove surrounding double quotes

print(f"[CONFIG] DATABASE_URL: {DATABASE_URL}")
print(f"[CONFIG] SECRET_KEY set: {bool(SECRET_KEY and SECRET_KEY != 'your-secret-key-change-in-production')}")

# ============= Database Setup =============
if "postgres" in DATABASE_URL.lower():
    from sqlalchemy.pool import QueuePool
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
    )
else:
    engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)

@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# ============= Models =============
class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255, index=True)
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)

class User(UserBase, table=True):
    __tablename__ = "user"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str
    password_confirm: str

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime

class LoginRequest(BaseModel):
    email: str
    password: str

class TodoBase(SQLModel):
    title: str = Field(nullable=False, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)

class Todo(TodoBase, table=True):
    __tablename__ = "todo"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

# ============= Authentication =============
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise ValueError("Password must be 72 bytes or less")
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {"user_id": uuid.UUID(user_id)}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload["user_id"]
    
    with get_session() as session:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user

# ============= FastAPI App =============
app = FastAPI(title="Todo Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    print("[STARTUP] Creating database tables...")
    create_db_and_tables()
    print("[STARTUP] Database tables created successfully")

# ============= Auth Routes =============
@app.post("/auth/register", response_model=UserRead, status_code=201)
def register(user_data: UserCreate):
    with get_session() as session:
        # Check if user exists
        existing = session.exec(select(User).where(User.email == user_data.email)).first()
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")
        
        if user_data.password != user_data.password_confirm:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        hashed = hash_password(user_data.password)
        db_user = User(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password_hash=hashed
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

@app.post("/auth/login", response_model=dict)
def login(login_data: LoginRequest):
    with get_session() as session:
        user = session.exec(select(User).where(User.email == login_data.email)).first()
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "created_at": user.created_at
            }
        }

@app.post("/auth/logout")
def logout():
    return {"message": "Logged out successfully"}

# ============= Todo Routes =============
@app.get("/todos", response_model=List[TodoRead])
@app.get("/todos/", response_model=List[TodoRead])
def get_todos(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    with get_session() as session:
        statement = select(Todo).where(Todo.user_id == current_user.id).offset(skip).limit(limit)
        todos = session.exec(statement).all()
        return todos

@app.post("/todos", response_model=TodoRead, status_code=201)
@app.post("/todos/", response_model=TodoRead, status_code=201)
def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user)
):
    with get_session() as session:
        db_todo = Todo(**todo_data.dict(), user_id=current_user.id)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

@app.get("/todos/{todo_id}", response_model=TodoRead)
def get_todo(
    todo_id: uuid.UUID,
    current_user: User = Depends(get_current_user)
):
    with get_session() as session:
        todo = session.exec(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
        ).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

@app.put("/todos/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: uuid.UUID,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user)
):
    with get_session() as session:
        todo = session.exec(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
        ).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        update_data = todo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)
        
        todo.updated_at = datetime.utcnow()
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: uuid.UUID,
    current_user: User = Depends(get_current_user)
):
    with get_session() as session:
        todo = session.exec(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
        ).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted successfully"}

@app.patch("/todos/{todo_id}/toggle-complete", response_model=TodoRead)
def toggle_todo_complete(
    todo_id: uuid.UUID,
    current_user: User = Depends(get_current_user)
):
    with get_session() as session:
        todo = session.exec(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
        ).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        todo.is_completed = not todo.is_completed
        todo.updated_at = datetime.utcnow()
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

# ============= Health Check =============
@app.get("/")
def read_root():
    return {
        "message": "Todo Management API running on Hugging Face Spaces",
        "status": "operational",
        "endpoints": {
            "auth": "/auth/register, /auth/login, /auth/logout",
            "todos": "/todos/, /todos/{id}",
            "chatbot": "/chatbot/chat, /chatbot/status"
        }
    }


# ============= AI Chatbot Feature =============
class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    action: Optional[Dict[str, Any]] = None
    action_result: Optional[Dict[str, Any]] = None


def get_system_prompt(todos: List[Dict[str, Any]]) -> str:
    """Generate system prompt with current todo context"""
    todos_json = json.dumps(todos, indent=2, default=str)
    
    return f"""You are an AI assistant integrated with a Todo Management application. 
You have access to the user's todos and can help them manage their tasks.

Current user's todos:
{todos_json}

You can help the user by:
1. Viewing and summarizing their todos
2. Suggesting which todos to prioritize
3. Helping organize tasks by category or urgency
4. Providing productivity tips
5. Answering questions about their tasks

When the user wants to:
- ADD a todo: Respond with a JSON object like: {{"action": "add", "title": "task title", "description": "optional description"}}
- UPDATE a todo: Respond with: {{"action": "update", "id": "todo-uuid", "title": "new title", "description": "new description", "is_completed": true/false}}
- DELETE a todo: Respond with: {{"action": "delete", "id": "todo-uuid"}}
- TOGGLE completion: Respond with: {{"action": "toggle", "id": "todo-uuid"}}
- Just chat or ask questions: Respond normally with helpful text

Always be concise, friendly, and helpful. If you need to perform an action, include the JSON at the end of your response.
"""


def execute_todo_action(action: Dict[str, Any], user_id: uuid.UUID, session: Session) -> Optional[Dict[str, Any]]:
    """Execute a todo action returned by the AI"""
    try:
        action_type = action.get('action')
        
        if action_type == 'add':
            todo_data = TodoCreate(
                title=action.get('title', 'Untitled'),
                description=action.get('description'),
                is_completed=action.get('is_completed', False)
            )
            db_todo = Todo(**todo_data.dict(), user_id=user_id)
            session.add(db_todo)
            session.commit()
            session.refresh(db_todo)
            return {
                "success": True,
                "message": f"Added todo: {db_todo.title}",
                "todo": {
                    "id": str(db_todo.id),
                    "title": db_todo.title,
                    "description": db_todo.description,
                    "is_completed": db_todo.is_completed
                }
            }
        
        elif action_type == 'update':
            todo_id = action.get('id')
            if not todo_id:
                return {"success": False, "message": "Todo ID required for update"}
            
            todo = session.exec(
                select(Todo).where(Todo.id == uuid.UUID(todo_id), Todo.user_id == user_id)
            ).first()
            if not todo:
                return {"success": False, "message": "Todo not found"}
            
            update_data = action.get('updates', {})
            if 'title' in update_data:
                todo.title = update_data['title']
            if 'description' in update_data:
                todo.description = update_data['description']
            if 'is_completed' in update_data:
                todo.is_completed = update_data['is_completed']
            
            todo.updated_at = datetime.utcnow()
            session.add(todo)
            session.commit()
            session.refresh(todo)
            return {
                "success": True,
                "message": f"Updated todo: {todo.title}",
                "todo": {
                    "id": str(todo.id),
                    "title": todo.title,
                    "description": todo.description,
                    "is_completed": todo.is_completed
                }
            }
        
        elif action_type == 'delete':
            todo_id = action.get('id')
            if not todo_id:
                return {"success": False, "message": "Todo ID required for delete"}
            
            todo = session.exec(
                select(Todo).where(Todo.id == uuid.UUID(todo_id), Todo.user_id == user_id)
            ).first()
            if not todo:
                return {"success": False, "message": "Todo not found"}
            
            session.delete(todo)
            session.commit()
            return {"success": True, "message": "Todo deleted successfully"}
        
        elif action_type == 'toggle':
            todo_id = action.get('id')
            if not todo_id:
                return {"success": False, "message": "Todo ID required for toggle"}
            
            todo = session.exec(
                select(Todo).where(Todo.id == uuid.UUID(todo_id), Todo.user_id == user_id)
            ).first()
            if not todo:
                return {"success": False, "message": "Todo not found"}
            
            todo.is_completed = not todo.is_completed
            todo.updated_at = datetime.utcnow()
            session.add(todo)
            session.commit()
            session.refresh(todo)
            return {
                "success": True,
                "message": f"{'Completed' if todo.is_completed else 'Reopened'}: {todo.title}",
                "todo": {
                    "id": str(todo.id),
                    "title": todo.title,
                    "is_completed": todo.is_completed
                }
            }
        
        return {"success": False, "message": "Unknown action type"}
        
    except Exception as e:
        return {"success": False, "message": f"Error executing action: {str(e)}"}


@app.post("/chatbot/chat", response_model=ChatResponse)
async def chat_with_bot(
    chat_data: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """Chat with the AI assistant that can help manage your todos"""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        return ChatResponse(
            response="AI chatbot is not configured. Please set GEMINI_API_KEY in the Hugging Face Space secrets.",
            action=None,
            action_result=None
        )
    
    try:
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Get user's todos for context
        with get_session() as session:
            statement = select(Todo).where(Todo.user_id == current_user.id)
            todos = session.exec(statement).all()
            todos_data = [
                {
                    "id": str(todo.id),
                    "title": todo.title,
                    "description": todo.description,
                    "is_completed": todo.is_completed,
                    "created_at": todo.created_at.isoformat()
                }
                for todo in todos
            ]
            
            system_prompt = get_system_prompt(todos_data)
            
            # Generate response using Gemini
            response = model.generate_content(
                f"{system_prompt}\n\nUser: {chat_data.message}\nAssistant:"
            )
            
            response_text = response.text.strip()
            
            # Check if response contains an action JSON
            action = None
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                try:
                    potential_action = json.loads(response_text[json_start:json_end])
                    if isinstance(potential_action, dict) and potential_action.get('action') in ['add', 'update', 'delete', 'toggle']:
                        action = potential_action
                        # Remove JSON from response text for cleaner display
                        response_text = response_text[:json_start].strip()
                except json.JSONDecodeError:
                    pass
            
            # Execute action if AI returned one
            action_result = None
            if action:
                action_result = execute_todo_action(action, current_user.id, session)
            
            return ChatResponse(
                response=response_text,
                action=action,
                action_result=action_result
            )
            
    except Exception as e:
        return ChatResponse(
            response=f"Sorry, I encountered an error: {str(e)}",
            action=None,
            action_result=None
        )


@app.get("/chatbot/status")
async def get_chatbot_status():
    """Get the chatbot configuration status"""
    api_key_configured = bool(os.getenv("GEMINI_API_KEY"))
    return {
        "configured": api_key_configured,
        "message": "Chatbot is ready" if api_key_configured else "Please set GEMINI_API_KEY environment variable"
    }

# ============= Main Entry Point =============
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    print(f"[MAIN] Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
