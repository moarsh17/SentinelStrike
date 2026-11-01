from db.database import SessionLocal
from events.models import EventModel
from ws.manager import manager
import asyncio
from datetime import datetime, timezone

async def record_and_broadcast_event(event_data: dict):
    # event_data should contain type, src_ip, dst_ip, dst_port, severity, details
    
    # Write to DB
    db = SessionLocal()
    try:
        new_event = EventModel(
            type=event_data.get("type"),
            src_ip=event_data.get("src_ip"),
            dst_ip=event_data.get("dst_ip"),
            dst_port=event_data.get("dst_port"),
            severity=event_data.get("severity"),
            details=event_data.get("details"),
            status="NEW",
            detected_at=datetime.now(timezone.utc)
        )
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        
        # Prepare for broadcast
        detected_iso = new_event.detected_at.isoformat()
        if not detected_iso.endswith("Z") and "+00:00" not in detected_iso:
            detected_iso += "Z"
            
        broadcast_data = {
            "id": new_event.id,
            "type": new_event.type,
            "src_ip": new_event.src_ip,
            "dst_ip": new_event.dst_ip,
            "dst_port": new_event.dst_port,
            "severity": new_event.severity,
            "status": new_event.status,
            "details": new_event.details,
            "detected_at": detected_iso
        }
    except Exception as e:
        print(f"Failed to record event to DB: {e}")
        return
    finally:
        db.close()
        
    # Broadcast to websocket clients
    await manager.broadcast_event(broadcast_data)
