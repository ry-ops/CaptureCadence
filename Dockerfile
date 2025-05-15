FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "capture_cadence.app:app", "--host", "0.0.0.0", "--port", "8000"]
