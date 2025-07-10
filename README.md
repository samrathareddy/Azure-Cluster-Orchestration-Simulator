# Azure Cluster Orchestration Simulator

A fully-featured orchestration simulator inspired by Azure Capacity Infrastructure Services (CIS), built with Python, FastAPI, and Docker. This tool models the lifecycle of cloud clusters—provisioning, refresh, and fault recovery—with telemetry, logging, and multi-cluster support.

---

## 🚀 Features

- 🔄 **Cluster Lifecycle Simulation**: Provision, refresh, and recover virtual clusters
- 🔐 **Basic Auth Security**: Protect access to orchestration and logs using username/password
- 📈 **Real-Time Dashboard**: Monitor orchestration flow and event counts with live Chart.js graphs
- 🌐 **Multi-Cluster Support**: Orchestrate multiple clusters with YAML-based playbooks
- 💾 **Persistent Logging**: Logs stored in JSON and downloadable as CSV
- 📦 **Dockerized**: Easily deployable locally or in cloud (Render, Azure App Service, etc.)
- 📥 **Downloadable Logs**: Export logs for any cluster via `/logs/download` API

---

## 🛠 Tech Stack

- **Python 3.10**
- **FastAPI**
- **Jinja2 Templates**
- **Chart.js**
- **Docker**
- **PyYAML**
- **HTTP Basic Auth**
- **Render Cloud Hosting (optional)**

---

## 🧱 Project Structure

```
azure_cluster_orchestration_simulator/
├── api.py                # FastAPI application with secured endpoints
├── cluster.py            # Core cluster lifecycle logic
├── orchestrator.py       # Playbook orchestration engine
├── telemetry.py          # Persistent telemetry logger (JSON & CSV)
├── utils.py              # Helper functions (delay, retry, locks)
├── templates/
│   └── dashboard.html    # Real-time UI with cluster controls
├── config/
│   ├── playbook-east.yaml
│   └── playbook-west.yaml
├── logs/
│   └── cluster-east.json / .csv
│   └── cluster-west.json / .csv
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## ⚙️ Usage

### 🔧 1. Clone & Install

```bash
git clone https://github.com/samrathareddy/Azure-Cluster-Orchestration-Simulator.git
cd Azure-Cluster-Orchestration-Simulator
pip install -r requirements.txt
```

### 🚀 2. Run Locally

```bash
uvicorn api:app --reload
```

Visit: `http://localhost:8000`

> Username and password are configured via `.env` file:
```
DASHBOARD_USER=admin
DASHBOARD_PASS=pass123
```

### 🐳 3. Docker Run

```bash
docker build -t azure-cluster-sim .
docker run -d -p 8000:8000 azure-cluster-sim
```

---

## 📊 Dashboard Features

- ✅ Select cluster: `cluster-east` or `cluster-west`
- ✅ Start orchestration from dropdown
- ✅ View real-time telemetry logs
- ✅ Chart showing provisioning, refresh, recovery counts
- ✅ Download logs as CSV via:
```
/logs/download?cluster=east
```

---

## 📝 License

MIT License

---

## 👨‍💻 Author

**Samratha Reddy**  
[GitHub](https://github.com/samrathareddy)
