import time
from collections import defaultdict
import asyncio
from ids.event_writer import record_and_broadcast_event

class SSHBruteForceDetector:
    def __init__(self, time_window=60, threshold=10):
        self.time_window = time_window
        self.threshold = threshold
        # Map: src_ip -> { "start_time": t, "count": 0, "cooldown_until": 0 }
        self.attempts = defaultdict(lambda: {"start_time": time.time(), "count": 0, "cooldown_until": 0})

    async def analyze_packet(self, packet):
        try:
            # Check if it's TCP traffic
            if hasattr(packet, 'tcp'):
                try:
                    dst_port = int(packet.tcp.dstport)
                except (ValueError, TypeError, AttributeError):
                    return

                # Target standard SSH ports (22, 2222)
                if dst_port in [22, 2222]:
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

                    # Detect TCP SYN packets (connection establishment attempts)
                    is_syn = False
                    if hasattr(packet.tcp, 'flags_syn') and str(packet.tcp.flags_syn) == '1':
                        is_syn = True
                    elif hasattr(packet.tcp, 'flags'):
                        try:
                            flag_val = int(str(packet.tcp.flags), 16)
                            if (flag_val & 0x02) != 0:  # SYN bit set
                                is_syn = True
                        except (ValueError, TypeError):
                            if str(packet.tcp.flags).strip() in ['0x0002', '0x02', '2']:
                                is_syn = True

                    if not is_syn:
                        return

                    current_time = time.time()
                    state = self.attempts[src_ip]

                    # Check alert cooldown
                    if current_time < state["cooldown_until"]:
                        state["start_time"] = current_time
                        return

                    if current_time - state["start_time"] > self.time_window:
                        state["start_time"] = current_time
                        state["count"] = 0

                    state["count"] += 1

                    if state["count"] >= self.threshold:
                        print(f"[!] SSH Brute-force detected from {src_ip} to {dst_ip} ({state['count']} attempts)")
                        await record_and_broadcast_event({
                            "type": "SSH_BRUTEFORCE",
                            "src_ip": src_ip,
                            "dst_ip": dst_ip,
                            "dst_port": dst_port,
                            "severity": "HIGH",
                            "details": f"Detected {state['count']} SSH connection attempts within {self.time_window}s window. Suppressing further alerts for 60s."
                        })
                        # Apply cooldown and reset count
                        state["cooldown_until"] = current_time + 60
                        state["count"] = 0
                        state["start_time"] = current_time

        except Exception as e:
            print(f"Error in SSHBruteForceDetector: {e}")

