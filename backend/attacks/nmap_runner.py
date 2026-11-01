import nmap
import asyncio

async def run_nmap_scan(target_ip: str):
    print(f"[*] Starting Nmap scan against {target_ip}...")
    nm = nmap.PortScanner()
    
    # Run in a separate thread so it doesn't block the async event loop
    loop = asyncio.get_event_loop()
    # -sS (SYN scan), -p 1-1000 (Ports 1 to 1000)
    # Using executor for blocking call
    result = await loop.run_in_executor(None, nm.scan, target_ip, '1-1000', '-sS')
    
    scan_results = []
    if target_ip in nm.all_hosts():
        for proto in nm[target_ip].all_protocols():
            lport = nm[target_ip][proto].keys()
            for port in lport:
                state = nm[target_ip][proto][port]['state']
                if state == 'open':
                    scan_results.append({"port": port, "state": state, "protocol": proto})
                    
    return scan_results
