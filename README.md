# Scientific Search MVP

A simple scientific text processing tool using Google Gemini AI for answering questions about scientific topics.

## Features

- FastAPI backend with Gemini AI integration
- React + TypeScript frontend with modern UI
- Simple REST API for asking scientific questions
- Real-time question answering with history tracking
- Automated testing with pytest
- CI/CD pipeline with GitHub Actions
- Docker containerization for deployment

## Technology Stack

**Backend:**

- Python 3.10+
- FastAPI - Fast, modern web framework
- Google Generative AI - Gemini API for text generation
- pytest - Testing framework

**Frontend:**

- React 19 - Modern UI library
- TypeScript - Type-safe JavaScript
- Vite - Fast build tool and dev server
- CSS3 - Modern styling with gradients and animations

**Justification of Technology Choices:**

- **Python**: Widely used in scientific computing, rich ecosystem for AI/ML
- **FastAPI**: High performance, automatic API documentation, type hints support
- **Gemini AI**: Advanced language model for scientific question answering
- **pytest**: Simple, powerful testing framework with excellent fixtures support
- **React + TypeScript**: Type-safe component-based UI with excellent developer experience
- **Vite**: Ultra-fast HMR (Hot Module Replacement) and optimized production builds

## Project Structure

```
scientific-search-mvp/
├── backend/              # Python FastAPI application
│   ├── src/             # Source code
│   │   ├── core/        # Core business logic
│   │   └── main.py      # FastAPI application entry point
│   ├── tests/           # Automated tests
│   └── requirements.txt # Python dependencies
├── frontend/            # React TypeScript application
│   ├── src/            # Source code
│   │   ├── App.tsx     # Main React component
│   │   ├── App.css     # Component styles
│   │   └── main.tsx    # Application entry point
│   ├── public/         # Static assets
│   └── package.json    # Node.js dependencies
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

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start development server:

```bash
npm run dev
```

4. Open browser at http://localhost:5173

The frontend will automatically connect to the backend API at `http://localhost:8000`.

## Docker Deployment

### Quick Start with Docker Compose

1. **Clone the repository:**

```bash
git clone https://github.com/snurmukhambet/scientific-search-mvp.git
cd scientific-search-mvp
```

2. **Set up environment variables:**

```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

3. **Run with Docker Compose:**

```bash
# Development mode
docker-compose up --build

# Production mode
docker-compose -f docker-compose.prod.yml up --build -d
```

4. **Access the application:**

- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Building Individual Images

**Backend:**

```bash
cd backend
docker build -t scientific-search-backend .
docker run -p 8000:8000 --env-file .env scientific-search-backend
```

**Frontend:**

```bash
cd frontend
docker build -t scientific-search-frontend .
docker run -p 80:80 scientific-search-frontend
```

### Container Features

- **Multi-stage builds** for optimized production images
- **Health checks** for both services
- **Security hardening** with non-root users
- **Nginx reverse proxy** for frontend with API routing
- **Volume mounts** for development
- **Network isolation** between services

## CI/CD Pipeline

This project uses **GitHub Actions** for automated CI/CD with the following features:

### Pipeline Stages

1. **Testing & Quality Assurance**

   - Backend: Unit tests with pytest, code coverage, linting with flake8, formatting with black
   - Frontend: ESLint linting, TypeScript type checking, build verification
   - Security: Trivy vulnerability scanning

2. **Build & Push**

   - Docker images built for both backend and frontend
   - Images pushed to Docker Hub with proper tagging
   - Multi-platform support and layer caching

3. **Deployment**
   - Automatic deployment to production environment
   - Environment-specific configurations
   - Rollback capabilities

### GitHub Actions Workflow

The pipeline is triggered on:

- Push to `main` or `develop` branches
- Pull requests to `main` branch

**Key features:**

- **Parallel execution** of backend and frontend tests
- **Dependency caching** for faster builds
- **Security scanning** with Trivy
- **Code coverage reporting** with Codecov
- **Docker layer caching** for efficient builds
- **Automatic Docker Hub publishing**

### Setting Up CI/CD

1. **Required GitHub Secrets:**

```bash
DOCKER_HUB_USERNAME=your_docker_username
DOCKER_HUB_TOKEN=your_docker_token
GEMINI_API_KEY=your_gemini_api_key
```

2. **Optional Secrets:**

```bash
SLACK_WEBHOOK_URL=your_slack_webhook_for_notifications
```

### Pipeline Configuration

The pipeline configuration is in `.github/workflows/ci-cd.yml` and includes:

- **Backend Tests**: Python 3.11, pytest with coverage, linting
- **Frontend Tests**: Node.js 18, ESLint, TypeScript checking
- **Security Scan**: Trivy for vulnerability detection
- **Docker Build**: Multi-stage builds with BuildKit
- **Deploy**: Configurable deployment target

### Local Testing

Run the same checks locally:

```bash
# Backend tests
cd backend
python -m pytest tests/ -v --cov=src
black --check src/ tests/
flake8 src/ tests/

# Frontend tests
cd frontend
npm run lint
npx tsc --noEmit
npm run build
```

## API Usage

### Using the Web Interface

1. Start the backend server (see Backend Setup)
2. Start the frontend development server (see Frontend Setup)
3. Open http://localhost:5173 in your browser
4. Enter your question in the text area and click "Отправить"
5. View the AI-generated answer and explore your question history

### Using curl

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

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Backend Run

```bash
# From backend directory
python run_server.py
# or
uvicorn src.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Frontend Run

```bash
# From frontend directory
npm run dev
```

### Quick Start (Both Services)

**Using Make (Recommended):**

```bash
# Development setup
make setup
cp .env.example backend/.env
# Edit backend/.env and add your Gemini API key

# Run with Docker
make docker-run

# Or run locally
make run
```

**Manual Setup:**

**Terminal 1 - Backend:**

```bash
cd backend
source venv/bin/activate  # if not activated
python run_server.py
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## Available Commands

Use `make help` to see all available commands:

```bash
make help              # Show all available commands
make build             # Build both frontend and backend
make test              # Run all tests
make lint              # Run linting for both projects
make docker-build      # Build Docker images
make docker-run        # Run with Docker Compose
make k8s-deploy        # Deploy to Kubernetes
```

## Production Deployment

### Kubernetes Deployment

1. **Prerequisites:**

   - Kubernetes cluster (minikube, EKS, GKE, etc.)
   - kubectl configured
   - Docker images built and pushed to registry

2. **Deploy:**

```bash
# Update the image tags in k8s/deployment.yml
make k8s-deploy

# Check status
make k8s-status

# Access the application
kubectl port-forward service/frontend-service 8080:80 -n scientific-search
```

3. **Cleanup:**

```bash
make k8s-delete
```

## Code Quality

This project includes comprehensive code quality tools:

- **Pre-commit hooks** for automated checks
- **Black** for Python code formatting
- **ESLint** for JavaScript/TypeScript linting
- **Flake8** for Python linting
- **Prettier** for frontend code formatting
- **Security scanning** with Trivy
- **Dependency vulnerability checks**

Setup pre-commit hooks:

```bash
make install-hooks
```

## License

MIT License - see LICENSE file for details.
