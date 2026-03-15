# energy-monitor-system
Test for DevOps Engineer candidates - Panoramic Power
# Energy Monitoring System - Home Assignment


# Energy Data Pipeline & Monitoring System

A distributed energy monitoring system built with a Microservices architecture, featuring a real-time data pipeline, automated scaling, and a web dashboard.

## 🚀 Architecture Overview
The system consists of the following components:
* **Frontend UI:** A web dashboard for submitting energy metrics (Nginx).
* **Ingestion API:** High-performance FastAPI service that receives data and pushes it to Redis.
* **Redis Streams:** Acts as a message broker and temporary storage.
* **Processing Worker:** A background service that consumes metrics, processes them, and maintains site history.
* **KEDA Autoscaler:** Automatically scales the worker fleet based on the Redis Stream backlog.



## 🛠 Tech Stack
* **Language:** Python (FastAPI, Redis-py)
* **Orchestration:** Kubernetes (K8s)
* **Package Management:** Helm
* **Infrastructure:** Redis Streams, KEDA
* **Containerization:** Docker

## 📦 Installation & Setup

### Prerequisites
* Kubernetes Cluster (Minikube / Docker Desktop)
* Helm 3+
* Docker Hub account

### Deployment
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd energy-monitoring-system
Deploy using Helm:

Bash
helm upgrade --install energy-app ./helm-chart
Expose the services:
Open two terminals and run:

Bash
# Terminal 1: API
kubectl port-forward svc/energy-app-ingestion-api 8000:80

# Terminal 2: Frontend UI
kubectl port-forward svc/energy-app-frontend-service 30080:80
Access the Dashboard:
Open your browser at http://localhost:30080