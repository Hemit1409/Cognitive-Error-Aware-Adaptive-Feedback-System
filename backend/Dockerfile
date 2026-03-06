FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run the pipeline to generate initial data, then start the server
CMD python ml_pipeline.py && uvicorn main:app --host 0.0.0.0 --port 8000
