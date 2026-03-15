import os
import logging
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from redis import Redis

# Using a logger for better K8s log management
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingestion_api")

app = FastAPI(title="Energy Data Ingestion Service")

# Redis connection details from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
r_client = Redis(host=REDIS_HOST, port=6379, decode_responses=True)

class MetricPayload(BaseModel):
    site_id: str
    device_id: str
    power_reading: float
    timestamp: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/readings", status_code=201)
async def ingest_metric(payload: MetricPayload):
    # Basic sanity check
    if not payload.site_id or not payload.device_id:
        logger.warning("Received a payload with missing site/device ID")
        raise HTTPException(status_code=422, detail="Incomplete data")

    try:
        # Pushing to a stream named 'raw_metrics'
        # xadd to ensure the message is persisted in Redis
        msg_id = r_client.xadd("raw_metrics", payload.dict())
        logger.info(f"Reading from site {payload.site_id} stored with ID: {msg_id}")
        
        return {"stream_id": msg_id}
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise HTTPException(status_code=500, detail="Internal storage error")