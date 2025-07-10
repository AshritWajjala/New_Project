FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

RUN apt update -y && apt install -y awscli

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (FastAPI default)
EXPOSE 8000

# Start FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
