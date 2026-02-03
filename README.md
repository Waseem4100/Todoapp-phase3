# Todo Management System

A full-stack web application for managing todos with user authentication and data persistence.

## Features

- User registration and authentication
- Create, read, update, and delete todos
- Mark todos as complete/incomplete
- User-specific data isolation
- Responsive web interface
- Secure API endpoints

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- Better Auth for authentication
- Alembic for database migrations

### Frontend
- Next.js
- React
- TypeScript
- Axios for API calls

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Git

## Installation

### Backend Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd todo-app/backend
```

2. Create virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Set up the database:
```bash
# For Neon PostgreSQL, create a new project and connection pool
# Update DATABASE_URL in .env with your Neon connection string
alembic upgrade head
```

5. Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup

1. Open a new terminal and navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

4. Start the development server:
```bash
npm run dev
```

## Running the Application

### Development Mode

1. Start the backend server (port 8000):
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

2. Start the frontend server (port 3000):
```bash
cd frontend
npm run dev
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## API Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /todos` - Get all user's todos
- `POST /todos` - Create a new todo
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a specific todo
- `DELETE /todos/{id}` - Delete a specific todo
- `PATCH /todos/{id}/toggle-complete` - Toggle todo completion status

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-secret-key-change-in-production
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Database Migrations

To create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

To apply migrations:
```bash
alembic upgrade head
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

## Security Features

- Password hashing using bcrypt
- JWT-based authentication
- User-specific data isolation
- Input validation
- Protection against common web vulnerabilities