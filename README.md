# Azure Cluster Orchestration Simulator

Simulates Azure-like cluster lifecycle automation—provisioning, refreshing, and fault recovery—using Python, with concurrency control, event-driven orchestration, telemetry logging, and playbook-based execution.

## 🚀 Project Overview

This simulator models how Azure Capacity Infrastructure Services (CIS) might orchestrate backend processes to manage distributed infrastructure. It’s designed for educational and demonstrative purposes.

### ✅ Features
- Event-driven lifecycle orchestration
- Cluster provisioning, refresh, and fault recovery
- Playbook-style automation (YAML)
- Telemetry and health logging
- Concurrency-safe operations with async locks
- Retry logic and fault injection
- Modular and extensible Python codebase

## 📁 Project Structure
```
azure_cluster_simulator/
├── main.py
├── cluster.py
├── orchestrator.py
├── telemetry.py
├── utils.py
├── config/
│   └── playbook.yaml
└── README.md
```

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/azure-cluster-orchestration-simulator.git
cd azure-cluster-orchestration-simulator
```

### 2. Install dependencies (Python 3.8+)
```bash
pip install -r requirements.txt
```

> Note: Only standard libraries (`asyncio`, `yaml`, `logging`) are used. You may need to install `pyyaml`:
```bash
pip install pyyaml
```

### 3. Run the simulator
```bash
python main.py
```

## 📖 Playbook Format
The `config/playbook.yaml` defines the cluster name and sequence of lifecycle operations:
```yaml
cluster_name: "azure-sim-cluster-01"

steps:
  - action: "provision"
    delay: 2
  - action: "refresh"
    delay: 3
  - action: "recover"
    delay: 2
```

## 📌 Future Improvements
- Web UI with FastAPI for real-time monitoring
- Cluster state dashboard
- Multi-cluster orchestration
- Metrics export to Prometheus/Grafana
- Docker-based simulation environments

## 🧑‍💻 Author
**Samratha Reddy**
Python | Cloud | Distributed Systems
[LinkedIn](https://www.linkedin.com/in/samrathareddy) | [GitHub](https://github.com/samrathareddy)

## 📝 License
This project is licensed under the MIT License.
