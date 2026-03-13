---
title: My Chatbot67
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: apache-2.0
short_description: RAG based ai model
---

# RAG Chatbot

A conversational chatbot with Retrieval-Augmented Generation (RAG) using LangChain, Pinecone, and Gemini.

## Quickstart

```bash
# Clone and enter project
git clone <your-repo-url>
cd chatbot-project

# Set up environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run
python run.py
```

Visit `http://localhost:5000` to chat.

## Project Structure

```
├── app/
│   ├── routes/          # API endpoints
│   ├── services/        # LLM, RAG, embedding logic
│   ├── templates/       # Chat UI
│   └── static/          # CSS, JS
├── config/              # App configuration
├── scripts/             # Utility scripts
├── tests/               # Pytest tests
├── docs/                # Documentation
├── .github/workflows/   # CI/CD
├── CLAUDE.md            # Claude Code instructions
├── requirements.txt     # Python dependencies
└── run.py               # Entry point
```

## Stack

| Layer       | Tool                          |
|-------------|-------------------------------|
| Backend     | Flask + LangChain             |
| LLM         | Gemini 2.5 Flash              |
| Embeddings  | HuggingFace sentence-transformers |
| Vector DB   | Pinecone                      |
| Hosting     | Render                        |
| CI/CD       | GitHub Actions                |

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
