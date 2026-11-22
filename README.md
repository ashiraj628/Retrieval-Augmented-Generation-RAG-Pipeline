# DocuMind : AI Document Search

AI Document Search is a Retrieval-Augmented Generation (RAG) application built using FastAPI. It allows users to upload PDF documents and ask questions about them in natural language. The application searches the uploaded documents for relevant information and uses the Google Gemini API to generate answers with source citations.

The project also includes user authentication, conversation history, background embedding generation, and semantic search using pgvector.

---

# Features

- User Registration & Login
- JWT Authentication (Access & Refresh Tokens)
- User-specific conversations
- Upload PDF documents
- Automatic PDF text extraction
- Background embedding generation using Dramatiq
- Semantic search with pgvector
- AI-generated answers using Google Gemini API
- Conversation history
- Source citations

---

# Tech Stack

### Backend

- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- pgvector

### AI

- Google Gemini API
- Sentence Transformers
- Retrieval-Augmented Generation (RAG)

### Other

- Dramatiq
- PyMuPDF
- JWT Authentication
- uv

---

# Installation

Clone the repository

```bash
git clone <repository-url>

cd AI-Document-Search
```

Create a virtual environment

```bash
uv venv
```

Install dependencies

```bash
uv sync
```

## Environment Variables

Create a `.env` file in the project root and add the following variables:

```env
APP_NAME=AI Document Search
API_V1_STR=/api/v1

DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/<database_name>

UPLOAD_DIR=storage

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.6-flash

SECRET_KEY=your_secret_key
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Run database migrations

```bash
alembic upgrade head
```

Start the FastAPI server

```bash
uv run uvicorn app.main:app --reload
```

Start the Dramatiq worker

```bash
uv run dramatiq app.workers.embedding --processes 1 --threads 1
```

---

# API Endpoints

## Authentication

### Register

**POST** `/auth/register`

Creates a new user account.

Request Body

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "password123"
}
```

Response

Returns the created user along with an access token and refresh token.

---

### Login

**POST** `/auth/login`

Logs in an existing user.

Request Body

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

Response

Returns an access token and refresh token.

---

### Refresh Access Token

**POST** `/auth/refresh`

Generates a new access token using a valid refresh token.

Authorization Header

```
Bearer <refresh_token>
```

---

### Get Current User

**GET** `/auth/me`

Returns information about the currently logged-in user.

Authorization Header

```
Bearer <access_token>
```

---

# Conversation Endpoints

All conversation endpoints require an access token.

---

### Create Conversation

**POST** `/conversations`

Creates a new conversation with the default title **"New chat"**.

No request body is required.

Response

```json
{
    "id": "conversation_uuid",
    "title": "New chat"
}
```

---

### List Conversations

**GET** `/conversations`

Returns all conversations created by the authenticated user.

Example Response

```json
[
  {
    "id": "...",
    "title": "Machine Learning Notes",
    "time": "2025-07-01T10:15:30"
  }
]
```

---

### Get Conversation

**GET** `/conversations/{conversation_id}`

Returns the selected conversation along with its complete message history.

---

### Delete Conversation

**DELETE** `/conversations/{conversation_id}`

Deletes the conversation and all associated data including uploaded documents, messages, chunks, and embeddings.

---

# Document Endpoint

### Upload PDF

**POST** `/conversations/{conversation_id}/documents`

Uploads a PDF document to a conversation.

Content Type

```
multipart/form-data
```

Form Data

| Field | Type | Required |
|-------|------|----------|
| file | PDF File | Yes |

After uploading, the application:

- Stores the PDF
- Extracts text
- Splits the text into chunks
- Saves the document information
- Starts a background worker to generate embeddings

---

# Chat Endpoint

### Ask a Question

**POST** `/chat`

Sends a question to the AI for an existing conversation.

The conversation must already exist. The frontend creates a new conversation using the **Create Conversation** endpoint before uploading documents or sending chat messages.

Request Body

```json
{
    "query": "What is machine learning?",
    "conversation_id": "conversation_uuid"
}
```

| Field | Description |
|-------|-------------|
| `query` | The user's question. |
| `conversation_id` | The ID of the conversation in which the question is being asked. |

Response

```json
{
    "answer": "...",
    "sources": [
        {
            "document_id": "...",
            "filename": "notes.pdf"
        }
    ],
    "conversation_id": "..."
}
```

--- 

# Authentication

Protected endpoints require an access token.

Example

```
Authorization: Bearer <access_token>
```

---

# How It Works

1. Create an account or log in.
2. Create a conversation.
3. Upload one or more PDF documents.
4. The document is processed and embeddings are generated in the background.
5. Ask questions related to the uploaded documents.
6. The application retrieves the most relevant document chunks and sends them to the Google Gemini API.
7. Gemini generates an answer, and the application returns the answer along with the source documents used.

---

# License
This project was created for learning and portfolio purposes.
