from fastapi import APIRouter, HTTPException
from core.config import settings
from .nmap_runner import run_nmap_scan
from .hydra_runner import run_hydra_attack
from .ml_password_generator import GenerativePasswordMutator, write_candidates_to_wordlist
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter(prefix="/attack", tags=["attack"])

class PasswordMutationRequest(BaseModel):
    brand_tokens: Optional[List[str]] = Field(default=["Sentinel", "Strike"])
    user_handle: Optional[str] = "admin"
    department: Optional[str] = "Security"
    year: Optional[str] = "2026"
    temperature: Optional[float] = 0.7
    count: Optional[int] = 12

class ApplyWordlistRequest(BaseModel):
    passwords: List[str]

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

@router.post("/generate-passwords")
async def generate_passwords(request: PasswordMutationRequest):
    try:
        mutator = GenerativePasswordMutator()
        candidates = mutator.generate(
            brand_tokens=request.brand_tokens,
            user_handle=request.user_handle,
            department=request.department,
            year=request.year,
            temperature=request.temperature,
            count=request.count
        )
        return {
            "status": "success",
            "model": "PassGAN & Char-RNN Structural Mutator (v1.0)",
            "parameters": {
                "brand_tokens": request.brand_tokens,
                "user_handle": request.user_handle,
                "department": request.department,
                "year": request.year,
                "temperature": request.temperature
            },
            "count": len(candidates),
            "candidates": candidates
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@router.post("/apply-wordlist")
async def apply_wordlist(request: ApplyWordlistRequest):
    if not request.passwords:
        raise HTTPException(status_code=400, detail="Password list cannot be empty")
    file_path = write_candidates_to_wordlist(request.passwords)
    return {
        "status": "success",
        "message": f"Successfully loaded {len(request.passwords)} candidate passwords into active attack wordlist.",
        "file": file_path
    }



