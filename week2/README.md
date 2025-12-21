# Action Intelligence | Intelligence Task Extractor

Action Intelligence is a local-first, AI-powered meeting notes assistant. It transforms unstructured narratives and messy meeting logs into clean, actionable to-do lists using a hybrid approach of traditional heuristics and Local LLMs (Ollama).

## 🚀 Features

- **Hybrid Extraction**: Uses ultra-fast regex-based heuristics for standard lists and falls back to a Large Language Model (Llama 3.1) for complex narrative text.
- **Smart Extract (LLM)**: Specifically identifies commitments and tasks in plain English sentences where traditional tools fail.
- **Notebook History**: Optionally archive your original notes to create a permanent record of context for every task.
- **Modern UI**: A premium, responsive dashboard with glassmorphism aesthetics and smooth interactions.
- **Privacy First**: Everything runs locally on your machine—no data ever leaves your computer.

---

## 🛠 Setup & Installation

### 1. Prerequisites
- **Python 3.10+** (managed via [Poetry](https://python-poetry.org/))
- **Ollama**: Download and install from [ollama.com](https://ollama.com)

### 2. Environment Setup
Clone the repository and install dependencies:
```bash
poetry install
```

### 3. Model Setup
Ensure the required model is available locally:
```bash
ollama pull llama3.1:8b
```

### 4. Running the Application
Start the uvicorn development server:
```bash
poetry run uvicorn week2.app.main:app --reload
```
Open your browser to [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 📡 API Endpoints

### Action Items
- `POST /action-items/extract`: Hybrid extraction (Heuristic first, fallback to LLM).
- `POST /action-items/extract-llm`: Force direct LLM extraction.
- `GET /action-items`: List all extracted tasks (optionally filtered by `note_id`).
- `POST /action-items/{id}/done`: Mark a task as complete or incomplete.

### Notes
- `GET /notes`: Retrieve all archived meeting notes.
- `POST /notes`: Manually save a new note entry.

---

## 🧪 Testing

The project includes a suite of tests for both the structural logic and the AI extraction.

### Run all tests:
```bash
# Ensure NO_PROXY is set if you use a VPN for localhost traffic
poetry run pytest week2/tests/test_extract.py
```

### Skip LLM Tests:
If you want to run only local logic without calling the LLM:
```bash
SKIP_LLM_TESTS=true poetry run pytest week2/tests/test_extract.py
```

---

## 🏗 Project Architecture

- `app/main.py`: Application entry point and lifespan management.
- `app/db.py`: Database session and operations layer.
- `app/schemas.py`: Pydantic models for request/response validation.
- `app/config.py`: Centralized configuration management.
- `app/services/extract.py`: The core logic for heuristic and LLM extraction.
- `app/routers/`: Organized API routing for Notes and Action Items.
