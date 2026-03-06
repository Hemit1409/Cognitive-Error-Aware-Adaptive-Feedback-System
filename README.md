# Cognitive Error-Aware Adaptive Feedback System

## Overview
This repository contains a full-stack, machine learning-based educational system designed to analyze student response patterns across longitudinal assessment sequences. It automatically infers latent cognitive error categories (like misconceptions and careless mistakes) and generates adaptive, targeted feedback tailored to each learner's diagnosed cognitive gap.

The system is split into two primary components:
1. **Python ML Pipeline & FastAPI Backend** (`/backend`)
2. **React + Vite + Tailwind Dashboard** (`/frontend`)

## Research Methodology (Abstract)
Current educational assessment systems are typically limited to correctness-based feedback, failing to understand *why* students err. This project proposes a data-driven approach to discover error *semantics*. Our pipeline extracts 20+ behavioral features (e.g., attempt counts, response time variability, error consistency) and applies K-Means and Agglomerative Hierarchical Clustering to identify interpretable taxonomic archetypes of student mistakes. Finally, each discovered error cluster is mapped to a dynamic adaptive feedback engine.

Evaluation via simulated Bayesian Knowledge Tracing demonstrates that targeting the *source* of the error (rather than just its correctness) yields significant gains in potential learning rate.

## Setup Instructions

### Option 1: Docker Compose (Recommended)
Ensure Docker Desktop is running, then simply execute:
```bash
docker-compose up --build
```
- The frontend will be available at `http://localhost:5173`
- The backend API will be available at `http://localhost:8000`

### Option 2: Local Manual Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the raw ML research script to generate metrics
python ml_pipeline.py

# Start the API server
uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints
- `GET /students` - List all students with error profiles.
- `GET /student/{id}` - Full error breakdown for a single student.
- `GET /clusters` - Cluster metadata and silhouette score evaluation.
- `GET /metrics` - Full evaluation report.
- `POST /predict` - Accepts raw response sequences and infers an error category.

## Sample Console Output
When running the ML pipeline standalone:
```
Generating Data...
Extracting Features...
Running Clustering...

--- Pipeline Metrics ---
{
    "silhouette_score": 0.48,
    "davies_bouldin": 0.85,
    "baseline_bkt_gain": 0.15,
    "adaptive_bkt_gain": 0.32,
    "relative_improvement": 113.33
}

Sample Output Feedback:
- "Misconception Errors": You seem to hold a consistent misconception on this topic...
- "Guessing Behavior": It looks like you might be rushing or guessing...
```
