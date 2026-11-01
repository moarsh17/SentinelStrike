from fastapi import APIRouter
from core.config import settings
from .nmap_runner import run_nmap_scan
from .hydra_runner import run_hydra_attack

router = APIRouter(prefix="/attack", tags=["attack"])

@router.post("/nmap-scan")
async def trigger_nmap_scan():
    target = settings.TEST_SERVER_IP
    results = await run_nmap_scan(target)
    return {"status": "completed", "target": target, "open_ports": results}

@router.post("/ssh-bruteforce")
async def trigger_ssh_bruteforce(port: int = 2222):
    target = settings.TEST_SERVER_IP
    results = await run_hydra_attack(target, port=port)
    return {"status": "completed", "target": target, "details": results}


