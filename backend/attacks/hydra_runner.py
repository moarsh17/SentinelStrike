import asyncio
import subprocess
import os
import shutil


async def _simulate_ssh_attempts(target_ip: str, port: int, users_file: str, passs_file: str):
    """
    Simulates high-frequency SSH connection attempts using raw asyncio sockets.
    This generates authentic TCP SYN and banner negotiation packets on the network interface,
    allowing the PyShark IDS to observe and detect brute-force activity even without external Hydra.
    """
    users = ["admin", "root", "testuser"]
    passwords = ["123456", "password", "admin123", "toor", "letmein", "welcome"]
    
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            users = [line.strip() for line in f if line.strip()]
            
    if os.path.exists(passs_file):
        with open(passs_file, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]

    log_lines = []
    attempt_count = 0

    # Ensure enough attempts to comfortably trigger IDS threshold (threshold=10)
    pairs = [(u, p) for u in users for p in passwords]
    if len(pairs) < 16:
        pairs = pairs * (16 // len(pairs) + 1)

    for user, pwd in pairs[:16]:
        attempt_count += 1
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(target_ip, port),
                timeout=0.8
            )
            # Send SSH client identification banner
            writer.write(b"SSH-2.0-SentinelStrike_Simulated_Client\r\n")
            await writer.drain()
            try:
                # Read server identification banner if available
                await asyncio.wait_for(reader.readline(), timeout=0.3)
            except Exception:
                pass
            log_lines.append(f"[Attempt {attempt_count}] User: '{user}' | Pass: '{pwd}' -> Auth Rejected (Permission Denied)")
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
        except Exception as e:
            log_lines.append(f"[Attempt {attempt_count}] User: '{user}' | Pass: '{pwd}' -> {type(e).__name__}")
        
        # Micro-delay between attempts to mimic automated dictionary tool
        await asyncio.sleep(0.04)

    return {
        "tool": "SentinelStrike Native SSH Simulator",
        "target": f"{target_ip}:{port}",
        "attempts_made": attempt_count,
        "output": "\n".join(log_lines),
        "return_code": 0
    }


async def run_hydra_attack(target_ip: str, port: int = 2222):
    print(f"[*] Starting SSH Brute-force against {target_ip}:{port}...")
    
    users_file = os.path.join(os.path.dirname(__file__), 'wordlists', 'users.txt')
    passs_file = os.path.join(os.path.dirname(__file__), 'wordlists', 'passwords.txt')
    
    # Check if hydra executable exists on the system PATH
    hydra_path = shutil.which("hydra")
    if not hydra_path:
        print("[!] Hydra binary not found in PATH. Executing native asynchronous SSH attack simulation...")
        return await _simulate_ssh_attempts(target_ip, port, users_file, passs_file)

    cmd = [
        "hydra",
        "-L", users_file,
        "-P", passs_file,
        "-t", "4",
        "-s", str(port),
        f"ssh://{target_ip}"
    ]
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        return {
            "tool": "hydra",
            "target": f"{target_ip}:{port}",
            "output": stdout.decode(errors='ignore'),
            "errors": stderr.decode(errors='ignore'),
            "return_code": process.returncode
        }
    except Exception as e:
        print(f"[!] Hydra execution failed: {e}. Falling back to native SSH simulation...")
        return await _simulate_ssh_attempts(target_ip, port, users_file, passs_file)

