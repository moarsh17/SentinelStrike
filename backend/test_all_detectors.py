import asyncio
import time
from ids.detectors.port_scan_detector import PortScanDetector
from ids.detectors.ssh_bruteforce_detector import SSHBruteForceDetector

class DummyTCPPacket:
    def __init__(self, dstport, flags='0x0002', flags_syn='1'):
        class TCP:
            pass
        class IP:
            pass
        self.tcp = TCP()
        self.ip = IP()
        self.tcp.dstport = dstport
        self.tcp.flags = flags
        self.tcp.flags_syn = flags_syn
        self.ip.src = '192.168.1.100'
        self.ip.dst = '192.168.1.200'

async def test_detectors():
    from db.database import engine, Base
    Base.metadata.create_all(bind=engine)
    print("=== Testing PortScanDetector ===")
    port_detector = PortScanDetector(time_window=10, threshold=10)
    for p in range(15):
        pkt = DummyTCPPacket(dstport=str(1000 + p))
        await port_detector.analyze_packet(pkt)
    print("Port scan test finished. Cooldown active:", port_detector.scan_state['192.168.1.100']['cooldown_until'] > time.time())

    print("\n=== Testing SSHBruteForceDetector ===")
    ssh_detector = SSHBruteForceDetector(time_window=60, threshold=5)
    for attempt in range(8):
        pkt = DummyTCPPacket(dstport='2222', flags='0x0002', flags_syn='1')
        await ssh_detector.analyze_packet(pkt)
    print("SSH brute force test finished. Cooldown active:", ssh_detector.attempts['192.168.1.100']['cooldown_until'] > time.time())
    print("\n[OK] Both detectors executed successfully without errors.")


if __name__ == '__main__':
    asyncio.run(test_detectors())
