# Quickstart Guide: Phase II - Todo Management System

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Git

## Environment Setup

### Backend Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd evolution-of-todo
```

2. Navigate to backend directory:
```bash
cd backend
```

3. Create virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Set up the database:
```bash
# For Neon PostgreSQL, create a new project and connection pool
# Update DATABASE_URL in .env with your Neon connection string
alembic upgrade head
```

6. Start the backend server:
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

### Production Build

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Serve the backend:
```bash
cd backend
gunicorn src.main:app
```

## Testing the Application

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## Key Configuration

### Database Configuration

The application uses Neon Serverless PostgreSQL. Update the `DATABASE_URL` in your environment variables:

```
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

### Authentication Configuration

Better Auth is configured with the following environment variables:

```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_TRUST_HOST=true
```

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

## Database Migrations

To create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

To apply migrations:
```bash
alembic upgrade head
```

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure your Neon PostgreSQL connection string is correct in the environment variables
2. **Port Conflicts**: Make sure ports 8000 (backend) and 3000 (frontend) are available
3. **Authentication**: Ensure the Better Auth configuration matches between frontend and backend
4. **CORS Issues**: Check that the allowed origins are properly configured in the backend

### Resetting Data

To reset the database (development only):
```bash
alembic downgrade base
alembic upgrade head
```

## Next Steps

1. Implement the authentication flow using Better Auth
2. Connect the frontend to the backend API
3. Add responsive design elements
4. Implement error handling and validation
5. Add loading states and user feedback