# energy-monitor-system
Test for DevOps Engineer candidates - Panoramic Power
# Energy Monitoring System - Home Assignment

## Overview
This project implements a scalable, microservices-based pipeline for ingesting and processing energy readings. The system is designed to handle high-throughput data using an event-driven architecture.

## Architecture & Design Decisions
The system is composed of two main services communicating through **Redis Streams**:

1.  **Ingestion API (FastAPI)**:
    - Responsible for receiving data from external sensors.
    - Uses **Pydantic** for schema validation to ensure data integrity before it enters the pipeline.
    - Handles requests asynchronously to maintain low latency.

2.  **Processing Service (Worker)**:
    - Consumes data from Redis using **Consumer Groups** to ensure "at-least-once" delivery.
    - Stores site-specific history for retrieval.
    - Uses **Acknowledgements (XACK)** to confirm successful processing, preventing data loss.

### Scaling Strategy (KEDA)
Instead of scaling based on CPU or Memory, I implemented **KEDA (Kubernetes Event-driven Autoscaling)**. 
- The system scales the Worker pods based on the **Redis Stream backlog** (`pendingEntriesCount`).
- This ensures that the system reacts to data spikes in real-time without wasting resources during idle periods.

### Security
- **Non-root containers**: Following security best practices, all Docker images are configured to run with a non-root user.
- **Resource Labeling**: All Kubernetes resources are labeled with the required assignment ID for tracking and management.

## Project Structure
- `src/ingestion-api/`: FastAPI application code and Dockerfile.
- `src/processing-service/`: Background worker code and Dockerfile.
- `charts/energy-app/`: Helm chart for full system deployment.

## Deployment Instructions

### 1. Build and Push Images
```bash
docker build -t noampaz26/energy-pipeline:ingestion-latest ./src/ingestion-api
docker push noampaz26/energy-pipeline:ingestion-latest

docker build -t noampaz26/energy-pipeline:worker-latest ./src/processing-service
docker push noampaz26/energy-pipeline:worker-latest

```



### 2. Deploy to Kubernetes via Helm

```bash
helm install energy-app ./charts/energy-app
```
