# azure_cluster_simulator/api.py

from fastapi import FastAPI, BackgroundTasks, Request, Depends, HTTPException, status, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from orchestrator import ClusterOrchestrator
from telemetry import TelemetryLogger
from dotenv import load_dotenv
import os
import secrets
import csv
import json

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

telemetry_loggers = {
    "east": TelemetryLogger("cluster-east"),
    "west": TelemetryLogger("cluster-west")
}

security = HTTPBasic()
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
async def run_orchestration(
    background_tasks: BackgroundTasks,
    cluster: str = Query("east"),
    creds: HTTPBasicCredentials = Depends(authenticate)
):
    playbook_file = f"config/playbook-{cluster}.yaml"

    async def run():
        orchestrator = ClusterOrchestrator(playbook_file, telemetry_loggers[cluster])
        await orchestrator.run_playbook()

    background_tasks.add_task(run)
    return {"message": f"Cluster '{cluster}' orchestration started."}

@app.get("/status")
def get_status(
    cluster: str = Query("east"),
    creds: HTTPBasicCredentials = Depends(authenticate)
):
    return {"status": f"Cluster '{cluster}' is running."}

@app.get("/logs")
def get_logs(
    cluster: str = Query("east"),
    creds: HTTPBasicCredentials = Depends(authenticate)
):
    return telemetry_loggers[cluster].events

@app.get("/logs/download")
def download_logs(
    cluster: str = Query("east"),
    creds: HTTPBasicCredentials = Depends(authenticate)
):
    log_path = f"logs/cluster-{cluster}.json"
    csv_path = f"logs/cluster-{cluster}.csv"

    if not os.path.exists(log_path):
        raise HTTPException(status_code=404, detail="Log file not found")

    with open(log_path, 'r') as json_file:
        logs = json.load(json_file)

    if logs:
        keys = logs[0].keys()
        with open(csv_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(logs)

    return FileResponse(path=csv_path, filename=f"{cluster}-telemetry.csv", media_type='text/csv')
