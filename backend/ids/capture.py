from core.config import settings
from .detectors.port_scan_detector import PortScanDetector
from .detectors.ssh_bruteforce_detector import SSHBruteForceDetector
import pyshark
import asyncio
import concurrent.futures

# Keep a global flag for graceful shutdown if needed
running = False

def pyshark_sniff_sync(main_loop, detectors):
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()
    
    import sys
    
    # CRITICAL FIX FOR WINDOWS: 
    # Background threads default to SelectorEventLoop which CANNOT run subprocesses (like tshark).
    # We MUST force ProactorEventLoop policy before creating the loop in this thread!
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
    # PyShark requires an event loop assigned to the thread
    asyncio.set_event_loop(asyncio.new_event_loop())

    def packet_callback(packet):
        if running:
            for detector in detectors:
                try:
                    future = asyncio.run_coroutine_threadsafe(detector.analyze_packet(packet), main_loop)
                    def on_done(fut, det_name=detector.__class__.__name__):
                        try:
                            fut.result()
                        except Exception as exc:
                            print(f"[!] Error in {det_name}: {exc}")
                    future.add_done_callback(on_done)
                except Exception as e:
                    print(f"[!] Callback error: {e}")
            
    try:
        capture = pyshark.LiveCapture(interface=settings.INTERFACE)
        # apply_on_packets handles its own internal loop execution safely
        capture.apply_on_packets(packet_callback)
    except Exception as e:
        print(f"[!] Capture error: {e}")

async def start_capture():
    global running
    running = True
    print(f"[*] Starting PyShark live capture on interface {settings.INTERFACE}...")
    
    detectors = [
        PortScanDetector(),
        SSHBruteForceDetector()
    ]
    
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, pyshark_sniff_sync, loop, detectors)

def stop_capture():
    global running
    running = False
    print("[*] Stopping PyShark capture...")
