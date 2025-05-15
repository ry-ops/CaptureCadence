# Dockerfile for backend
FROM python:3.11-slim

WORKDIR /app

# Copy everything inside backend folder to /app in container
COPY . .

# Install dependencies from requirements.txt without caching
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
