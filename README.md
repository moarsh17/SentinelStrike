# SentinelStrike

> **Automated Network Attack Simulation and Real-Time Intrusion Detection**  
> *A unified Purple Team security platform combining offensive security testing with packet-level intrusion detection.*

---

## ⚡ Quick Start

### 1. Backend (FastAPI + PyShark IDS)
```bash
cd backend
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python test_all_detectors.py
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Frontend (Next.js 16 Dashboard)
```bash
cd frontend
npm install
npm run dev
```
Visit **[http://localhost:3000](http://localhost:3000)**.

### 3. Or Run with Docker Compose
```bash
docker-compose up --build
```

---

## 📖 Complete Documentation & Manual

For an in-depth breakdown of the architecture, newly added features, custom Machine Learning integration blueprints, and demo scripts, consult:
📄 **[SENTINEL_STRIKE_MANUAL.md](./SENTINEL_STRIKE_MANUAL.md)**

---

## 🛡️ Supported Attack & Detection Vectors

| Attack Vector | Tool / Mechanism | Detection Logic | Severity |
|---|---|---|---|
| **Port Scanning** | Nmap / Connect Scans | Sliding Window + Unique Port Count Threshold | `HIGH` |
| **SSH Brute-Force** | Hydra / Async TCP Socket Simulator | High-Frequency TCP SYN Tracking on SSH Ports (22/2222) | `HIGH` |
| **Future: Web Fuzzing** | Gobuster / Directory Enumeration | HTTP 404 Burst Detection | `MEDIUM` |
| **Future: DoS / Flood** | SYN Flood / Slowloris | Half-open connection tracking | `CRITICAL` |
