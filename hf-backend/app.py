import sys
import os

# Add the project root and src directory to the Python path to allow proper imports
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')

# Insert paths at the beginning to ensure they're found first
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Todo Management API", version="1.0.0")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enhanced import and register routes with detailed error reporting
try:
    logger.info("Attempting to import route modules...")
    
    # Verify directory structure exists
    logger.info(f"Project root: {project_root}")
    logger.info(f"Src path: {src_path}")
    logger.info(f"Src exists: {os.path.exists(src_path)}")
    logger.info(f"Src/api exists: {os.path.exists(os.path.join(src_path, 'api'))}")
    logger.info(f"Src/api/routes exists: {os.path.exists(os.path.join(src_path, 'api', 'routes'))}")
    
    # Import routes with explicit paths
    import src.api.routes.auth
    import src.api.routes.todos
    
    # Get the routers from the imported modules
    auth_router = src.api.routes.auth.router
    todos_router = src.api.routes.todos.router
    
    logger.info("Successfully imported route routers")

    # Include API routes
    app.include_router(auth_router, prefix="/auth", tags=["authentication"])
    app.include_router(todos_router, prefix="/todos", tags=["todos"])

except ImportError as e:
    logger.error(f"Detailed import error: {e}")
    logger.error(f"Python path: {sys.path}")
    logger.error(f"Current directory: {os.getcwd()}")
    
    # Log directory structure for debugging
    try:
        logger.error(f"Directory contents: {os.listdir('.')}")
        if os.path.exists('src'):
            logger.error(f"Src directory contents: {os.listdir('src')}")
            if os.path.exists('src/api'):
                logger.error(f"Src/api directory contents: {os.listdir('src/api')}")
                if os.path.exists('src/api/routes'):
                    logger.error(f"Src/api/routes directory contents: {os.listdir('src/api/routes')}")
    except Exception as dir_e:
        logger.error(f"Error listing directories: {dir_e}")
    
    from fastapi import APIRouter
    # Create fallback routers with error messages
    auth_router = APIRouter()
    todos_router = APIRouter()

    @auth_router.get("/")
    def auth_error():
        return {"error": f"Auth routes not available: {e}", "debug_info": {
            "cwd": os.getcwd(),
            "python_path": sys.path,
            "src_exists": os.path.exists(src_path),
            "api_routes_exists": os.path.exists(os.path.join(src_path, 'api', 'routes'))
        }}

    @todos_router.get("/")
    def todos_error():
        return {"error": f"Todo routes not available: {e}"}

    # Still include the routers but with error messages
    app.include_router(auth_router, prefix="/auth", tags=["authentication"])
    app.include_router(todos_router, prefix="/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Todo Management API running on Hugging Face Spaces", "status": "operational"}

# Try to set up database if possible
try:
    from sqlmodel import SQLModel
    from src.database.database import engine

    @app.on_event("startup")
    def on_startup():
        try:
            # Create database tables
            logger.info("Creating database tables...")
            SQLModel.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            # Don't crash the app if database initialization fails
            pass
except ImportError as e:
    logger.error(f"Failed to import database components: {e}")

from fastapi.responses import JSONResponse

# Error handling
@app.exception_handler(404)
async def not_found_error(request, exc):
    logger.error(f"404 error for path: {request.url.path}")
    return JSONResponse(status_code=404, content={"detail": f"Resource not found: {request.url.path}"})

@app.exception_handler(500)
async def internal_error(request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.exception_handler(TypeError)
async def type_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": f"Type error: {str(exc)}"})

# For Hugging Face Spaces compatibility
def start_server():
    port = int(os.getenv("PORT", 7860))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    start_server()