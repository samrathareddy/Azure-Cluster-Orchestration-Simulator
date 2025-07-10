# azure_cluster_simulator/api.py

from fastapi import FastAPI, BackgroundTasks, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from orchestrator import ClusterOrchestrator
from telemetry import TelemetryLogger
from cluster import ClusterManager
from dotenv import load_dotenv
import asyncio
import yaml
import os
import secrets

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

telemetry_logger = TelemetryLogger()
cluster = None
security = HTTPBasic()

# Environment credentials
USERNAME = os.getenv("DASHBOARD_USER", "admin")
PASSWORD = os.getenv("DASHBOARD_PASS", "pass123")

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/", response_class=HTMLResponse)
def root(request: Request, creds: HTTPBasicCredentials = Depends(authenticate)):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/run")
async def run_orchestration(background_tasks: BackgroundTasks, creds: HTTPBasicCredentials = Depends(authenticate)):
    async def run():
        orchestrator = ClusterOrchestrator("config/playbook.yaml")
        await orchestrator.run_playbook()
    background_tasks.add_task(run)
    return {"message": "Cluster orchestration started."}

@app.get("/status")
def get_status(creds: HTTPBasicCredentials = Depends(authenticate)):
    global cluster
    if cluster is None:
        return {"status": "Cluster not initialized"}
    return {
        "name": cluster.name,
        "status": cluster.status,
        "nodes": cluster.nodes
    }

@app.get("/logs")
def get_logs(creds: HTTPBasicCredentials = Depends(authenticate)):
    return telemetry_logger.events
