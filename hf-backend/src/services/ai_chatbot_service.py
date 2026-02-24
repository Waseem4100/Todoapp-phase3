import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import google.generativeai as genai
from sqlmodel import Session
from uuid import UUID

from src.models.todo import Todo, TodoCreate, TodoUpdate
from src.services.todo_service import TodoService


class AIChatbotService:
    """Service for handling AI chatbot interactions with todo management capabilities"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the chatbot service with Gemini API key"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        else:
            self.model = None
    
    def _get_system_prompt(self, todos: List[Dict[str, Any]]) -> str:
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

    async def chat(self, message: str, user_id: UUID, session: Session) -> Dict[str, Any]:
        """
        Process a chat message and return AI response with potential todo actions
        
        Args:
            message: User's message
            user_id: ID of the current user
            session: Database session
            
        Returns:
            Dictionary with 'response' text and optional 'action' to perform
        """
        if not self.model:
            return {
                "response": "AI chatbot is not configured. Please set up your GEMINI_API_KEY in the environment variables.",
                "action": None
            }
        
        # Get user's todos for context
        todos = TodoService.get_user_todos(session, user_id)
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
        
        system_prompt = self._get_system_prompt(todos_data)
        
        try:
            # Generate response using Gemini
            response = self.model.generate_content(
                f"{system_prompt}\n\nUser: {message}\nAssistant:"
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
            
            return {
                "response": response_text,
                "action": action
            }
            
        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "action": None
            }
    
    def execute_action(self, action: Dict[str, Any], user_id: UUID, session: Session) -> Optional[Dict[str, Any]]:
        """
        Execute a todo action returned by the AI
        
        Args:
            action: Action dictionary from AI response
            user_id: ID of the current user
            session: Database session
            
        Returns:
            Result of the action or None if action is invalid
        """
        try:
            action_type = action.get('action')
            
            if action_type == 'add':
                todo_data = TodoCreate(
                    title=action.get('title', 'Untitled'),
                    description=action.get('description'),
                    is_completed=action.get('is_completed', False)
                )
                todo = TodoService.create_todo(session, todo_data, user_id)
                return {
                    "success": True,
                    "message": f"Added todo: {todo.title}",
                    "todo": {
                        "id": str(todo.id),
                        "title": todo.title,
                        "description": todo.description,
                        "is_completed": todo.is_completed
                    }
                }
            
            elif action_type == 'update':
                todo_id = action.get('id')
                if not todo_id:
                    return {"success": False, "message": "Todo ID required for update"}
                
                update_data = TodoUpdate(
                    title=action.get('title'),
                    description=action.get('description'),
                    is_completed=action.get('is_completed')
                )
                todo = TodoService.update_todo(session, UUID(todo_id), update_data, user_id)
                if todo:
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
                return {"success": False, "message": "Todo not found"}
            
            elif action_type == 'delete':
                todo_id = action.get('id')
                if not todo_id:
                    return {"success": False, "message": "Todo ID required for delete"}
                
                success = TodoService.delete_todo(session, UUID(todo_id), user_id)
                return {
                    "success": success,
                    "message": "Todo deleted successfully" if success else "Todo not found"
                }
            
            elif action_type == 'toggle':
                todo_id = action.get('id')
                if not todo_id:
                    return {"success": False, "message": "Todo ID required for toggle"}
                
                todo = TodoService.toggle_todo_completion(session, UUID(todo_id), user_id)
                if todo:
                    return {
                        "success": True,
                        "message": f"{'Completed' if todo.is_completed else 'Reopened'}: {todo.title}",
                        "todo": {
                            "id": str(todo.id),
                            "title": todo.title,
                            "is_completed": todo.is_completed
                        }
                    }
                return {"success": False, "message": "Todo not found"}
            
            return {"success": False, "message": "Unknown action type"}
            
        except Exception as e:
            return {"success": False, "message": f"Error executing action: {str(e)}"}
