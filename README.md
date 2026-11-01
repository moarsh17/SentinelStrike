# SentinelStrike

> **Automated Purple Team Platform: Offensive Simulation, Real-Time Intrusion Detection & AI Credential Intelligence**  
> *A unified cybersecurity platform bridging adversarial testing with packet-level traffic analysis.*

---

## ⚡ Overview

**SentinelStrike** combines offensive security simulation with deep packet-level intrusion detection and machine learning-powered credential intelligence in a unified, modern platform.

Rather than managing disjointed tools across multiple terminals, SentinelStrike provides an integrated system where you can:
1. **Synthesize Targeted Wordlists** using an AI-driven Generative Password Mutation model (PassGAN / Char-RNN).
2. **Execute Controlled Attacks** (Nmap port scans, SSH dictionary attacks) from an offensive dashboard.
3. **Capture & Detect Threats in Real Time** via a live PyShark packet sniffer analyzing raw network traffic.
4. **Stream Alerts Instantly** to a reactive Next.js 16 cyber-themed monitoring dashboard over WebSockets.

---

## 🏗️ Architecture & Data Flow

```
                      ┌──────────────────────────────────────────────┐
                      │             Next.js 16 Dashboard             │
                      │  (Offensive Hub, AI Mutator, Event Feed/Log) │
                      └──────────────┬────────────────▲──────────────┘
                                     │                │
            POST /attack/nmap-scan   │                │ WebSocket (/ws)
            POST /attack/ssh-bruteforce               │ Real-Time Alert Broadcast
            POST /attack/generate-passwords           │
                                     │                │
                                     ▼                │
   ┌──────────────────────────────────────────────────┴───────────────────────────────────┐
   │                                  FastAPI Backend                                     │
   │                                                                                      │
   │   ┌────────────────────────┐                   ┌─────────────────────────────────┐   │
   │   │    Offensive Module    │                   │       Defensive IDS Module      │   │
   │   │  - Nmap Scanner        │                   │   - PyShark Live Packet Sniffer │   │
   │   │  - Hydra / Native SSH  │                   │   - PortScanDetector (Window)   │   │
   │   │  - AI Credential Mutator                   │   - SSHBruteForceDetector (SYN) │   │
   │   └───────────┬────────────┘                   └────────────────▲────────────────┘   │
   │               │                                                 │                    │
   │               │ Executes Network Traffic                        │ Sniffs Raw Packets │
   │               ▼                                                 │ on Loopback / eth0 │
   │   ┌────────────────────────┐                                    │                    │
   │   │ Native SSH / Victim Box│ ═══════════════════════════════════╛                    │
   │   │ 127.0.0.1 : Port 2222  │                                                         │
   │   └────────────────────────┘                   ┌─────────────────────────────────┐   │
   │                                                │     PostgreSQL / SQLite DB      │   │
   │                                                │         (events table)          │   │
   │                                                └─────────────────────────────────┘   │
   └──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Core Modules & Implemented Features

### 1. 🧠 AI Credential Intelligence (PassGAN & Char-RNN Structural Mutator)
- **Concept**: Instead of brute-forcing generic `rockyou.txt` lists, this model trains on human credential behavior (Probabilistic Context-Free Grammars + Character Transitions).
- **Inputs**: Organizational metadata (`Brand Tokens`, `User Handle`, `Department`, `Year`, `Mutation Temperature`).
- **Engine**: Probabilistically applies character substitution matrices (`a->@`, `e->3`, `s->$`, `t->7`), casing permutations, structural delimiters, and human-like affixes.
- **Analytics**: Calculates **Shannon Entropy** ($H$) in bits and **Human Likelihood Match** percentage for every generated candidate.
- **Direct Injection**: One-click **"Apply to Live Attack"** button loads the generated corpus directly into the active SSH dictionary runner.

### 2. ⚔️ Offensive Controller
- **Nmap Reconnaissance**: Launches TCP SYN host discovery and service port scans across ports 1–1000.
- **SSH Dictionary Brute-Force**: 
  - Dual-mode execution: Spawns `hydra` if installed in PATH, or seamlessly falls back to a **native asynchronous raw-socket attack engine**.
  - Generates authentic TCP SYN packets and SSH protocol identification handshakes (`SSH-2.0-SentinelStrike_Client`).
  - No external Docker required: FastAPI includes a built-in lightweight SSH mock daemon on port `2222`.

### 3. 🛡️ Defensive IDS Engine (PyShark / TShark)
- **Port Scan Detector**: Sliding-window heuristic tracking connections to $> 15$ unique destination ports within 10 seconds.
- **SSH Brute-Force Detector**: Tracks high-frequency TCP SYN attempts targeting ports `22` and `2222` ($\ge 10$ attempts).
- **Anti-Flood Alert Suppression**: Enforces a 60-second cooldown per source IP upon raising a `HIGH` alert to protect SIEM databases from alert fatigue.

### 4. 📊 Unified Monitoring Dashboard
- **Offensive Controller Panel**: Interactive scan triggers, live execution status, and terminal log inspection.
- **AI Credential Mutator Studio**: Form controls, temperature slider, entropy metrics, and wordlist applicator.
- **Live Threat Stream**: WebSocket-driven alert banner with severity badges (`HIGH`, `MEDIUM`, `LOW`).
- **Historical Event Log**: Persistent alert query table with column filtering and database timestamps.

---

## 🚀 Quick Start Guide

### Option 1: Native Local Run (Windows / macOS / Linux)

#### 1. Backend (FastAPI + PyShark IDS)
```powershell
cd backend
python -m venv .venv

# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt

# Run integration detector tests
python test_all_detectors.py

# Launch FastAPI server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
> *The backend automatically starts the native mock SSH service on `127.0.0.1:2222` and starts the PyShark sniffer on your loopback adapter.*

#### 2. Frontend (Next.js 16 Dashboard)
```powershell
cd frontend
npm install
npm run dev
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser.

---

### Option 2: Docker Compose (Full Stack)

To run PostgreSQL, the backend, and the Ubuntu 22.04 test server in an isolated container network:

```bash
docker-compose up --build
```

---

## 🕹️ End-to-End Demo Workflow

1. **Open Dashboard**: Navigate to `http://localhost:3000`. Confirm the header displays `IDS Sniffer Active` and `PassGAN / Char-RNN v1.0`.
2. **Synthesize AI Credentials**:
   - In the **Credential AI Mutator** panel, enter target metadata:
     - Brand: `Sentinel, Strike`
     - User: `admin`
     - Department: `Security`
     - Year: `2026`
     - Temperature: `0.70`
   - Click **"Synthesize Wordlist"**. Observe candidate passwords generated with entropy ratings and human likelihood scores.
   - Click **"Apply to Live Attack"** to inject the candidates into the active wordlist.
3. **Launch SSH Brute-Force**:
   - Under the Offensive Controller, click **"Launch SSH Brute-force Attack"**.
   - Review the execution output in the terminal log.
   - Within seconds, PyShark detects the connection burst and raises an **`SSH_BRUTEFORCE`** alert on the live feed.
4. **Launch Nmap Recon Scan**:
   - Click **"Launch Nmap Recon Scan"**.
   - The sniffer detects the multi-port probe pattern and raises a **`PORT_SCAN`** alert.
5. **Verify Persistence**:
   - Check the **Historical Event Log** to confirm all incidents are recorded with UTC timestamps, source IP, target IP, port, and severity.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/attack/nmap-scan` | Executes Nmap SYN port scan against target |
| `POST` | `/attack/ssh-bruteforce?port=2222` | Triggers SSH brute-force attack |
| `POST` | `/attack/generate-passwords` | Generates AI-mutated passwords from target metadata |
| `POST` | `/attack/apply-wordlist` | Injects candidate passwords into the active attack wordlist |
| `GET` | `/events/` | Fetches historical security alerts from database |
| `WS` | `/ws` | Real-time WebSocket connection for live alert broadcasts |

---

## 📂 Repository Structure

```
SentinelStrike/
├── README.md                                  # Repository documentation
├── SENTINEL_STRIKE_MANUAL.md                  # Comprehensive manual & ML blueprint
├── docker-compose.yml                         # Docker orchestration
├── .gitignore                                 # Root Git exclusions
│
├── backend/                                   # FastAPI Service
│   ├── main.py                                # App entrypoint, mock SSH daemon, WebSocket
│   ├── .gitignore                             # Backend Git exclusions
│   ├── requirements.txt                       # Python dependencies
│   ├── test_all_detectors.py                  # Integration test suite
│   ├── core/config.py                         # Settings (DB_URL, INTERFACE, TARGET)
│   ├── attacks/
│   │   ├── router.py                          # Attack & AI generation routes
│   │   ├── ml_password_generator.py           # PassGAN / Char-RNN generative model
│   │   ├── hydra_runner.py                    # Hydra / native async socket engine
│   │   ├── nmap_runner.py                     # Nmap execution runner
│   │   └── wordlists/                         # Wordlist directory
│   ├── ids/
│   │   ├── capture.py                         # PyShark capture engine
│   │   ├── event_writer.py                    # DB commit & WebSocket dispatcher
│   │   └── detectors/
│   │       ├── port_scan_detector.py          # Port scan detection heuristic
│   │       └── ssh_bruteforce_detector.py     # SSH brute-force detection heuristic
│   └── events/                                # Event models & history routes
│
├── frontend/                                  # Next.js 16 Web Application
│   ├── .gitignore                             # Frontend Git exclusions
│   ├── package.json
│   ├── app/
│   │   ├── page.tsx                           # Main command dashboard
│   │   └── components/
│   │       ├── AttackControls.tsx             # Offensive scan & brute-force buttons
│   │       ├── PasswordGenerator.tsx          # AI Credential Mutator UI
│   │       ├── EventFeed.tsx                  # Real-time alert stream
│   │       └── EventTable.tsx                 # Historical alerts table
│   └── lib/
│       ├── apiClient.ts                       # REST API client
│       └── wsClient.ts                        # WebSocket connection client
│
└── test-server/                               # Victim Box
    └── Dockerfile                             # Optional Ubuntu 22.04 SSH test container
```
