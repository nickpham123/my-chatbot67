# RAG Chatbot

Python/Flask chatbot with LangChain RAG pipeline, Pinecone vector store, and DeepSeek/Gemini LLM.

## Commands
- `python -m venv venv` — Create virtual environment
- `source venv/bin/activate` — Activate venv (Linux/Mac)
- `venv\Scripts\activate` — Activate venv (Windows)
- `pip install -r requirements.txt` — Install dependencies
- `pip freeze > requirements.txt` — Update dependencies
- `python run.py` — Start Flask dev server (port 5000)
- `pytest tests/` — Run all tests
- `pytest tests/test_chat.py -v` — Run specific test file

## Architecture
- `/app/` — Flask application (factory pattern with `create_app()`)
  - `/app/routes/` — API route blueprints (chat, documents, health)
  - `/app/services/` — Business logic (llm_service, rag_service, embedding_service)
  - `/app/templates/` — Jinja2 HTML templates (chat UI)
  - `/app/static/` — CSS and JS assets
- `/config/` — App configuration (env-based: dev, prod)
- `/scripts/` — Utility scripts (document ingestion, Pinecone setup)
- `/tests/` — Pytest test files
- `/docs/` — Project documentation
- `.github/workflows/` — GitHub Actions CI/CD

## Stack
- **Backend**: Flask + LangChain
- **LLM**: DeepSeek V3.2 (OpenAI-compatible API) — cheapest option
  - Alt: Gemini Flash free tier for development
- **Embeddings**: HuggingFace sentence-transformers (free, runs locally)
- **Vector DB**: Pinecone (free tier — 1 index, 100K vectors)
- **Database**: Supabase PostgreSQL (conversation history, user data)
- **Hosting**: Render (free tier for dev, $7/mo for prod)
- **CI/CD**: GitHub Actions

## Code Style
- Python 3.10+
- Use type hints on all function signatures
- Use Google-style docstrings
- Prefer f-strings over .format()
- Keep functions short — if it's over 30 lines, break it up
- Use environment variables for all secrets (never hardcode)

## Environment Variables
All secrets go in `.env` (never commit this file):
- `DEEPSEEK_API_KEY` — LLM API key
- `PINECONE_API_KEY` — Pinecone API key
- `PINECONE_INDEX_NAME` — Pinecone index name
- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_KEY` — Supabase anon key
- `FLASK_SECRET_KEY` — Flask session secret
- `FLASK_ENV` — development or production

## Git Conventions
- Branch naming: `feature/description`, `fix/description`
- Commit format: `feat: add chat endpoint`, `fix: embedding timeout`
- Always create a branch for new features, never push directly to main

## Important Notes
- LangChain changes APIs frequently — pin versions in requirements.txt
- DeepSeek uses OpenAI-compatible API, so use `ChatOpenAI` with custom `base_url`
- Pinecone free tier has a 100K vector limit — monitor usage in dashboard
- Run `pytest` before every commit
- The `/health` endpoint should always return 200 — Render uses it for health checks

## Phase Plan
1. Basic Flask + LangChain + DeepSeek chat (no RAG)
2. Add Pinecone RAG pipeline (upload, embed, query)
3. Frontend chat UI + conversation history (Supabase)
4. Deploy to Render
5. CI/CD with GitHub Actions
6. (Future) Migrate to AWS for resume/learning
