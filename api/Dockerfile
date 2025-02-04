FROM python:3.11

WORKDIR /app

# Copying backend files
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Running FastAPI app
CMD ["uvicorn", "api_backend:app", "--host", "0.0.0.0", "--port", "8000"]
