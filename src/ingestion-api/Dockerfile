FROM python:3.12-slim

# Creating a non-root user for security
RUN useradd -m ingestion_user
WORKDIR /home/ingestion_user

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensuring the user owns the directory
RUN chown -R ingestion_user:ingestion_user /home/ingestion_user
USER ingestion_user

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]