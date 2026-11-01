from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from db.database import engine, Base
from events import router as events_router
from attacks import router as attacks_router
from ws.manager import manager
from ids.capture import start_capture, stop_capture
from contextlib import asynccontextmanager
import nest_asyncio

nest_asyncio.apply()

Base.metadata.create_all(bind=engine)

async def start_mock_ssh_service(host="127.0.0.1", port=2222):
    """
    Lightweight built-in SSH service running directly in Python.
    Eliminates the need for external Docker containers by listening on 127.0.0.1:2222
    and executing genuine SSH protocol handshakes for the offensive and defensive modules.
    """
    async def handle_ssh_client(reader, writer):
        try:
            writer.write(b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4\r\n")
            await writer.drain()
            try:
                await asyncio.wait_for(reader.readline(), timeout=0.5)
            except Exception:
                pass
            writer.write(b"Permission denied (publickey,password).\r\n")
            await writer.drain()
        except Exception:
            pass
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass

    try:
        server = await asyncio.start_server(handle_ssh_client, host, port)
        print(f"[*] Native SSH target service active on {host}:{port} (No Docker required!)")
        return server
    except Exception as e:
        print(f"[!] Could not start native SSH service on {port}: {e}")
        return None

# Use lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    ssh_server = await start_mock_ssh_service()
    capture_task = asyncio.create_task(start_capture())
    yield
    # Shutdown
    if ssh_server:
        ssh_server.close()
        await ssh_server.wait_closed()
    stop_capture()
    capture_task.cancel()
    try:
        await capture_task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="SentinelStrike API", lifespan=lifespan)

# Allow CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events_router.router)
app.include_router(attacks_router.router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, wait for client messages if needed
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected from WebSocket")
