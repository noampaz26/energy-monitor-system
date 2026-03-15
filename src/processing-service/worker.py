import os
import time
import threading
from redis import Redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() # Used for health probes and data retrieval

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_host = os.getenv("REDIS_HOST", "localhost")
r = Redis(host=redis_host, port=6379, decode_responses=True)

STREAM_NAME = "raw_metrics"
GROUP_NAME = "metrics_processors"
# use the hostname (Pod name) as the consumer ID
CONSUMER_ID = os.getenv("HOSTNAME", "local-worker")

def init_redis():
    """ Initialize the consumer group if it doesn't exist yet """
    try:
        r.xgroup_create(STREAM_NAME, GROUP_NAME, id="0", mkstream=True)
        print(f"[*] Group {GROUP_NAME} initialized.")
    except:
        print(f"[*] Group {GROUP_NAME} already exists.")

def start_processing():
    init_redis()
    while True:
        try:
            # Block for 2 seconds if no new messages are found
            results = r.xreadgroup(GROUP_NAME, CONSUMER_ID, {STREAM_NAME: ">"}, count=1, block=2000)
            
            if not results:
                continue

            for _, messages in results:
                for m_id, data in messages:
                    # Save the data to a site-specific list for history
                    r.lpush(f"history:site:{data['site_id']}", str(data))
                    
                    # Acknowledge the message so it's removed from PEL
                    r.xack(STREAM_NAME, GROUP_NAME, m_id)
                    print(f"[ACK] Processed site {data['site_id']} reading {m_id}")

        except Exception as e:
            print(f"[!] Error in processing loop: {e}")
            time.sleep(5)

# Run the worker in a background thread
threading.Thread(target=start_processing, daemon=True).start()

@app.get("/sites/{site_id}")
def get_site_readings(site_id: str):
    # Fetch all stored readings for a specific site
    return r.lrange(f"history:site:{site_id}", 0, -1)

@app.get("/health")
def health(): return {"status": "up"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)