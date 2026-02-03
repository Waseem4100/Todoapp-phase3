# Data Model: Phase II - Todo Management System

## User Entity

**Fields**:
- `id`: UUID (Primary Key, Auto-generated)
- `email`: String (Required, Unique, Email format validation)
- `password_hash`: String (Required, Encrypted)
- `first_name`: String (Optional)
- `last_name`: String (Optional)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated, Updates on change)

**Relationships**:
- One-to-Many: User → Todos (user owns multiple todos)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must meet minimum strength requirements
- First and last name must not exceed 50 characters

## Todo Entity

**Fields**:
- `id`: UUID (Primary Key, Auto-generated)
- `title`: String (Required, Max 200 characters)
- `description`: Text (Optional, Max 1000 characters)
- `is_completed`: Boolean (Default: False)
- `user_id`: UUID (Foreign Key, References User.id)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated, Updates on change)

**Relationships**:
- Many-to-One: Todo → User (todo belongs to one user)

**Validation Rules**:
- Title is required and cannot be empty
- Title must be between 1 and 200 characters
- Description cannot exceed 1000 characters
- Todo must belong to a valid user
- Only the owning user can modify or delete the todo

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Todos table
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_is_completed ON todos(is_completed);
CREATE INDEX idx_users_email ON users(email);
```

## State Transitions

**Todo Completion States**:
- Pending (is_completed = False) → Completed (is_completed = True)
- Completed (is_completed = True) → Pending (is_completed = False)

**User Account States**:
- Unverified (after registration) → Active (after email verification)
- Active → Suspended (admin action - not currently implemented in Phase II)

## Constraints

**Data Integrity**:
- Foreign key constraints ensure referential integrity
- Unique constraint on user email
- Cascade delete on user removal (deletes associated todos)
- Non-null constraints on required fields

**Security**:
- Passwords stored as hashed values (never plaintext)
- User ID associated with each todo for access control
- Soft deletes not implemented (todos are permanently deleted)