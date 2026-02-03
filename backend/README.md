# Todo App Backend

This is the backend for the Todo Management System built with FastAPI and Python.

## Local Development

To run the backend locally:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
uvicorn src.main:app --reload --port 8000
```

## Environment Variables

The following environment variables are required:

```
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Deployment to Railway

This application is configured for deployment to Railway. To deploy:

1. Connect your Railway account to your GitHub repository
2. Create a new Railway project
3. Select this repository
4. Railway will automatically detect this is a Python app and build it
5. Add the required environment variables in the Railway dashboard
6. Deploy!

### Required Environment Variables on Railway:
- `DATABASE_URL`: PostgreSQL connection string (can use Railway's managed PostgreSQL)
- `SECRET_KEY`: Secret key for JWT tokens (generate a strong random key)

## API Documentation

Once deployed, API documentation will be available at `/docs` endpoint.

## Database Setup

The application uses SQLModel with PostgreSQL. On Railway:
1. Add a PostgreSQL addon to your project
2. Use the automatically generated DATABASE_URL environment variable
3. The application will automatically create tables on startup