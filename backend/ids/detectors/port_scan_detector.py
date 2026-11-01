import time
from collections import defaultdict
import asyncio
from ids.event_writer import record_and_broadcast_event

class PortScanDetector:
    def __init__(self, time_window=10, threshold=15):
        self.time_window = time_window
        self.threshold = threshold
        # Map: src_ip -> { "start_time": t, "ports": set(), "cooldown_until": 0 }
        self.scan_state = defaultdict(lambda: {"start_time": time.time(), "ports": set(), "cooldown_until": 0})

    async def analyze_packet(self, packet):
        try:
            # Look for TCP packets (often used in port scans)
            if hasattr(packet, 'tcp'):
                src_ip = None
                dst_ip = None
                if hasattr(packet, 'ip'):
                    src_ip = packet.ip.src
                    dst_ip = packet.ip.dst
                elif hasattr(packet, 'ipv6'):
                    src_ip = packet.ipv6.src
                    dst_ip = packet.ipv6.dst
                    
                if not src_ip:
                    return
                    
                dst_port = int(packet.tcp.dstport)
                
                state = self.scan_state[src_ip]
                current_time = time.time()
                
                # If we recently alerted on this IP, ignore new packets until cooldown expires
                if current_time < state["cooldown_until"]:
                    # Keep shifting the window forward so it doesn't instantly fire when cooldown ends
                    state["start_time"] = current_time
                    return
                
                if current_time - state["start_time"] > self.time_window:
                    # Reset window
                    state["start_time"] = current_time
                    state["ports"] = set()
                
                state["ports"].add(dst_port)
                
                if len(state["ports"]) > self.threshold:
                    print(f"[!] Port scan detected from {src_ip} to {dst_ip}")
                    await record_and_broadcast_event({
                        "type": "PORT_SCAN",
                        "src_ip": src_ip,
                        "dst_ip": dst_ip,
                        "dst_port": None,
                        "severity": "HIGH",
                        "details": f"Detected scans to {len(state['ports'])} unique ports. Suppressing further alerts for 60s."
                    })
                    
                    # Apply a 60-second cooldown for this source IP
                    state["cooldown_until"] = current_time + 60
                    # Reset state
                    state["ports"] = set()
                    state["start_time"] = current_time
                        
        except Exception as e:
            print(f"Error in PortScanDetector: {e}") # Debugging error
