# Scientific Search MVP

A simple scientific text processing tool using Google Gemini AI for answering questions about scientific topics.

## Features

- FastAPI backend with Gemini AI integration
- Simple REST API for asking scientific questions
- Automated testing with pytest
- CI/CD pipeline with GitHub Actions

## Technology Stack

**Backend:**
- Python 3.10+
- FastAPI - Fast, modern web framework
- Google Generative AI - Gemini API for text generation
- pytest - Testing framework

**Justification of Technology Choices:**
- **Python**: Widely used in scientific computing, rich ecosystem for AI/ML
- **FastAPI**: High performance, automatic API documentation, type hints support
- **Gemini AI**: Advanced language model for scientific question answering
- **pytest**: Simple, powerful testing framework with excellent fixtures support

## Project Structure

```
scientific-search-mvp/
├── backend/              # Python FastAPI application
│   ├── src/             # Source code
│   │   ├── core/        # Core business logic
│   │   └── main.py      # FastAPI application entry point
│   ├── tests/           # Automated tests
│   └── requirements.txt # Python dependencies
├── .github/
│   └── workflows/       # CI/CD pipeline configuration
└── README.md
```

## Setup and Installation

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp ../.env.example .env
# Edit .env and add your Gemini API key
```

5. Run the application:
```bash
python run_server.py
```

6. API will be available at http://localhost:8000
   - Documentation: http://localhost:8000/docs

## Testing

Run automated tests:
```bash
cd backend
python -m pytest tests/ -v
```

## API Usage

### Ask a Scientific Question

```bash
curl -X POST "http://localhost:8000/api/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is machine learning?"}'
```

## CI/CD Pipeline

The project uses GitHub Actions for automated testing of both backend and frontend:

**Backend Pipeline:**
- **Testing**: Runs pytest on every push/PR
- **Code Quality**: Checks formatting with Black and linting with Flake8

**Frontend Pipeline:**
- **Linting**: ESLint code quality checks
- **Build**: TypeScript compilation and Vite build process

**Infrastructure:**
- **Cross-platform**: Tests on Ubuntu latest
- **Node.js 18** and **Python 3.10** environments

## Development

### Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run
```bash
uvicorn src.main:app --reload
```

## License

MIT License - see LICENSE file for details.