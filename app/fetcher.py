"""
Beacon fetcher — a trivial worker reused from the Sentinel pipeline.

The business logic is intentionally minimal. The POINT is the instrumentation:
this service exposes a Prometheus /metrics endpoint so Beacon has something
real to scrape, dashboard, and alert on.

Run locally:  uvicorn fetcher:app --host 0.0.0.0 --port 8000
Metrics at:   http://localhost:8000/metrics
"""
import os
import time
import random
import asyncio
import logging

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("beacon")

# --- Metrics: the three signals the Grafana dashboard is built on ---
FETCHES = Counter("beacon_fetches_total", "Total fetch cycles attempted")
ERRORS = Counter("beacon_fetch_errors_total", "Total fetch cycles that failed")
DURATION = Histogram(
    "beacon_fetch_duration_seconds",
    "Time spent per fetch cycle",
    buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0),
)

# Injecting a failure rate lets you trigger the Phase 5 alert on demand.
FAILURE_RATE = float(os.getenv("BEACON_FAILURE_RATE", "0.02"))

app = FastAPI(title="Beacon Fetcher")


def do_one_fetch() -> None:
    """Simulate one unit of pipeline work, recording metrics."""
    start = time.perf_counter()
    FETCHES.inc()
    try:
        # stand-in for "fetch a URL / read from Postgres / push to Redis"
        time.sleep(random.uniform(0.05, 0.4))
        if random.random() < FAILURE_RATE:
            raise RuntimeError("simulated downstream failure")
    except Exception as exc:  # noqa: BLE001
        ERRORS.inc()
        log.error("fetch failed: %s", exc)
    finally:
        DURATION.observe(time.perf_counter() - start)


async def worker_loop() -> None:
    """Background loop so the service always has live metrics to scrape."""
    while True:
        do_one_fetch()
        await asyncio.sleep(1)


@app.on_event("startup")
async def startup() -> None:
    log.info("beacon fetcher starting (failure_rate=%.3f)", FAILURE_RATE)
    asyncio.create_task(worker_loop())


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
