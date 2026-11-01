import pyshark
import threading
import nmap

def nmap_scan():
    nm = nmap.PortScanner()
    nm.scan('127.0.0.1', '8000-8010', '-sS')

cap = pyshark.LiveCapture(interface=r'\Device\NPF_Loopback')
t = threading.Thread(target=nmap_scan)
t.start()

cap.sniff(packet_count=1, timeout=5)
for p in cap:
    print("TCP layer dir:", dir(p.tcp))
    print("Has IP:", hasattr(p, 'ip'))
    print("Has IPv6:", hasattr(p, 'ipv6'))
    print("IP src:", getattr(p.ip, 'src', None) if hasattr(p, 'ip') else getattr(p.ipv6, 'src', None))
    print("Dst port:", p.tcp.dstport)
