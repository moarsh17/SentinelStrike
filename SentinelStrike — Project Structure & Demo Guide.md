# SentinelStrike — Project Structure & Demo Guide

Automated Network Attack Simulation and Real-Time Intrusion Detection **Stack: FastAPI (backend) + Next.js (frontend)**

---

## 1. What It Does

A local Purple Team platform: launch controlled attacks (Nmap scan, Hydra SSH brute-force) from a web dashboard against a designated test server, while a packet-sniffing IDS detects the attack pattern in real traffic and raises an alert on the same dashboard within seconds.

Since both the attack controller and the PyShark IDS are Python-native, they now live in **one FastAPI service** instead of a separate Node.js controller — simpler stack, one less moving part.

```
 Dashboard (Next.js)
     │  "Launch Nmap Scan"  (HTTP POST)
     ▼
 FastAPI Backend
     ├── Attack Module  ──► runs Nmap/Hydra against Test Server
     └── IDS Module (PyShark) ──► sniffs traffic ──► detects pattern ──► writes event
                                                              │
                                                              ▼
                                                        PostgreSQL
                                                              │
     ◄──────────────────── WebSocket push ────────────────────
     ▼
 Dashboard ──► alert appears live
```

---

## 2. Minimal Project Structure (for a basic demo build)

```
sentinelstrike/
├── README.md
├── docker-compose.yml                # postgres + optional test-server container
│
├── backend/                          # FastAPI service (attacks + IDS + API + WebSocket)
│   ├── requirements.txt              # fastapi, uvicorn, pyshark, psycopg2, python-nmap
│   ├── main.py                       # FastAPI app entrypoint, mounts routers + WS
│   ├── core/
│   │   └── config.py                 # TEST_SERVER_IP, DB_URL, allowed scan range
│   │
│   ├── attacks/                      # Offensive Controller module
│   │   ├── router.py                 # POST /attack/nmap-scan, /attack/ssh-bruteforce
│   │   ├── nmap_runner.py            # spawns nmap, parses output
│   │   ├── hydra_runner.py           # spawns hydra with test wordlist
│   │   └── wordlists/
│   │       └── test-ssh-users.txt
│   │
│   ├── ids/                          # Traffic Analysis / Intrusion Detection module
│   │   ├── capture.py                # PyShark capture loop (runs as background task)
│   │   ├── detectors/
│   │   │   ├── port_scan_detector.py      # SYN/connect scan heuristic
│   │   │   └── ssh_bruteforce_detector.py # repeated auth-failure heuristic
│   │   └── event_writer.py           # inserts detected events into PostgreSQL
│   │
│   ├── events/                       # Security Event module
│   │   ├── router.py                 # GET /events (history from Postgres)
│   │   └── models.py                 # Pydantic + SQLAlchemy event models
│   │
│   ├── ws/
│   │   └── manager.py                # WebSocket connection manager, broadcasts new events
│   │
│   └── db/
│       └── schema.sql                # events table: id, type, src, dst, port,
│                                      # severity, status, detected_at
│
├── frontend/                         # Unified Monitoring Dashboard (Next.js)
│   ├── package.json
│   ├── app/
│   │   ├── page.tsx                  # main dashboard view
│   │   └── components/
│   │       ├── AttackControls.tsx    # buttons: Run Nmap / Run Hydra
│   │       ├── EventFeed.tsx         # live alert list (WebSocket)
│   │       └── EventTable.tsx        # historical events from GET /events
│   └── lib/
│       ├── apiClient.ts              # calls FastAPI REST endpoints
│       └── wsClient.ts               # connects to FastAPI WebSocket
│
└── test-server/                      # the authorized "victim" box
    ├── Dockerfile                    # lightweight SSH-enabled image
    └── sshd_config
```

---

## 3. Demo Build Priority (if time is limited)

Build in this order so there's always something demoable:

1. **test-server** — a container with SSH exposed and a couple of open ports
2. **backend/ids/** — get PyShark capturing + one detector (port scan) working, printing to console
3. **backend/db/** — wire the detector to write to PostgreSQL
4. **backend/attacks/** — Nmap route first (simplest attack to trigger)
5. **frontend/** — static event table calling `GET /events` (no WebSocket yet)
6. **backend/ws/** — make alerts appear live, no refresh
7. **Hydra route + brute-force detector** — second attack type, same pipeline

Steps 1–5 alone are enough for a basic demo (click → attack runs → event appears, even on refresh). Steps 6–7 turn it into the full "live" version described in the synopsis.

---

## 4. Demo Script for Professor

| Step | Action | What to Point Out |
| --- | --- | --- |
| 1 | Show empty dashboard + FastAPI logs | IDS capture loop is running as a background task, no events yet |
| 2 | Click "Launch Nmap Scan" | Show real Nmap output in a terminal alongside |
| 3 | Watch dashboard | Alert appears within seconds via WebSocket — explain the traffic pattern that triggered it |
| 4 | Click "Launch SSH Brute-force" | Show Hydra attempting the test wordlist |
| 5 | Watch dashboard | Second alert type appears — explain the auth-failure threshold logic |
| 6 | Query/refresh | Prove events persisted in PostgreSQL, not just pushed live |
| 7 | Q&A | Be ready to explain detection thresholds, scope (local/authorized-only tool), and why attacks + IDS share one FastAPI process |

---

## 5. Tech Stack Reference

| Layer | Technology |
| --- | --- |
| Attack execution | Nmap, Hydra |
| Traffic capture/analysis | PyShark (Python) |
| Event storage | PostgreSQL |
| Backend | **FastAPI** (Python) — attacks, IDS, REST API, WebSocket, all in one service |
| Frontend | Next.js, React, Tailwind CSS |
| Real-time updates | WebSockets (native FastAPI support) |