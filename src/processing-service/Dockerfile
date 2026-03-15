FROM python:3.12-slim

# Creating a non-root user for security
RUN useradd -m worker_user
WORKDIR /home/worker_user

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensuring the user owns the directory
RUN chown -R worker_user:worker_user /home/worker_user
USER worker_user


CMD ["python", "worker.py"]