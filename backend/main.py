from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import json
import os
from ml_pipeline import CognitiveErrorFeedbackSystem

app = FastAPI(title="Cognitive Error-Aware Adaptive Feedback API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to generate data or load it
pipeline = CognitiveErrorFeedbackSystem()

@app.on_event("startup")
async def startup_event():
    print("Initializing Cognitive Feedback Pipeline...")
    pipeline.generate_synthetic_data()
    pipeline.extract_features()
    pipeline.discover_clusters()
    pipeline.generate_feedback_templates()
    pipeline.evaluate()
    print("Pipeline initialization complete.")

@app.get("/students")
def get_students():
    # Return list of students with error profiles
    df = pipeline.features_df[['student_id', 'total_errors', 'inferred_taxonomy', 'true_error_type']]
    return df.to_dict(orient="records")

@app.get("/student/{student_id}")
def get_student_detail(student_id: int):
    # Full error breakdown
    student_feats = pipeline.features_df[pipeline.features_df['student_id'] == student_id]
    if student_feats.empty:
        return {"error": "Student not found"}
        
    student_dict = student_feats.iloc[0].to_dict()
    student_dict = {k: float(v) if isinstance(v, (float, int, np.integer, np.floating)) else v for k, v in student_dict.items()}
    
    # Get raw responses
    responses = pipeline.df[pipeline.df['student_id'] == student_id].to_dict(orient="records")
    responses = [{k: float(v) if isinstance(v, (float, int, np.integer, np.floating)) else v for k, v in r.items()} for r in responses]
    
    # Feedback
    taxonomy = student_dict['inferred_taxonomy']
    feedback = pipeline.feedback_bank.get(taxonomy, {})
    
    return {
        "profile": student_dict,
        "responses": responses,
        "feedback": feedback
    }

@app.get("/clusters")
def get_clusters():
    # Return cluster metadata
    counts = pipeline.features_df['inferred_taxonomy'].value_counts().to_dict()
    return {
        "metrics": pipeline.metrics,
        "cluster_sizes": counts
    }

@app.get("/metrics")
def get_metrics():
    # Return full evaluation report
    return pipeline.evaluate()

class ResponseSequence(BaseModel):
    responses: list

@app.post("/predict")
def predict_sequence(req: ResponseSequence):
    taxonomy, confidence = pipeline.predict_new_sequence(req.responses)
    feedback = pipeline.feedback_bank.get(taxonomy, {})
    return {
        "inferred_taxonomy": taxonomy,
        "confidence": float(confidence),
        "feedback": feedback
    }
