import asyncio
import time
from ids.detectors.port_scan_detector import PortScanDetector

class DummyPacket:
    def __init__(self, dstport):
        class TCP:
            pass
        class IP:
            pass
        self.tcp = TCP()
        self.ip = IP()
        self.tcp.dstport = dstport
        self.ip.src = '127.0.0.1'
        self.ip.dst = '127.0.0.1'

async def main():
    detector = PortScanDetector()
    for i in range(20):
        await detector.analyze_packet(DummyPacket(str(8000 + i)))
        print(f"Added port {8000 + i}, length is now {len(detector.scan_state['127.0.0.1']['ports'])}")

asyncio.run(main())
