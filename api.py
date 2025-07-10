# azure_cluster_simulator/api.py

from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cluster import ClusterManager
from telemetry import TelemetryLogger
from orchestrator import ClusterOrchestrator
import asyncio
import yaml

app = FastAPI()
templates = Jinja2Templates(directory="templates")

telemetry_logger = TelemetryLogger()
cluster = None

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/run")
async def run_orchestration(background_tasks: BackgroundTasks):
    async def run():
        orchestrator = ClusterOrchestrator("config/playbook.yaml")
        await orchestrator.run_playbook()
    background_tasks.add_task(run)
    return {"message": "Cluster orchestration started."}

@app.get("/status")
def get_status():
    global cluster
    if cluster is None:
        return {"status": "Cluster not initialized"}
    return {
        "name": cluster.name,
        "status": cluster.status,
        "nodes": cluster.nodes
    }

@app.get("/logs")
def get_logs():
    return telemetry_logger.events
