
# Smart Note Taker API 🧠

A production-ready FastAPI backend for the Smart Note Taking Agent. Features AI-powered classification (Gemini/OpenAI/Ollama), Notion integration, and Clerk authentication.

## Features
- **FastAPI Architecture**: Modular, scalable, and async.
- **AI Processing**: Uses LangGraph to classify notes, tasks, and ideas.
- **Voice Support**: Integrated OpenAI Whisper for audio transcription.
- **Authentication**: Secure Clerk.dev integration with JWKS verification.
- **Database**: SQLModel + SQLite for efficient local storage.
- **Notion Sync**: Automatically organizes content into your Notion workspace.

## Setup

1. **Install Dependencies**
   ```bash
   uv sync
   ```

2. **Environment Variables**
   Ensure your `.env` file has:
   ```env
   # API Keys
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=...
   NOTION_API_KEY=secret_...
   NOTION_PAGE_ID=...
   
   # Clerk Auth
   CLERK_SECRET_KEY=sk_...
   CLERK_PUBLISHABLE_KEY=pk_...
   CLERK_ISSUER=https://<your-domain>.clerk.accounts.dev
   ```

3. **Run the Server**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

## API Documentation
Once running, visit:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure
```text
app/
├── api/            # Route handlers
├── core/           # Config & Security
├── db/             # Database connection
├── models/         # SQLModel database schemas
├── schemas/        # Pydantic API schemas
├── services/       # Business logic (LLM, Notion, Voice)
└── utils/          # Helper functions
```
