import pyshark
import threading
import nmap
import time

def nmap_scan():
    print("Nmap thread starting, waiting 2s...")
    time.sleep(2)
    print("Nmap scanning...")
    nm = nmap.PortScanner()
    nm.scan('127.0.0.1', '8000-8020', '-sS')
    print("Nmap finished.")

count = 0
def packet_callback(packet):
    global count
    count += 1
    if count == 15:
        print("Got 15 packets via apply_on_packets!")

cap = pyshark.LiveCapture(interface=r'\Device\NPF_Loopback')
t = threading.Thread(target=nmap_scan)
t.start()

print("Starting apply_on_packets...")
cap.apply_on_packets(packet_callback, timeout=10)
print(f"Total packets captured: {count}")
