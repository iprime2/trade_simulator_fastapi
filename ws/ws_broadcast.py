from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from ws.ws_client import latest_orderbook
from loguru import logger
import asyncio

router = APIRouter()
clients = []

@router.websocket("/ws/tick")
async def tick_websocket(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    logger.info(f"[FRONTEND_WS] Client connected. Total: {len(clients)}")

    try:
        while True:
            await asyncio.sleep(1)  # Push every second
            await websocket.send_json(latest_orderbook)
    except WebSocketDisconnect:
        clients.remove(websocket)
        logger.warning(f"[FRONTEND_WS] Client disconnected. Total: {len(clients)}")
    except Exception as e:
        logger.exception("[FRONTEND_WS] Error in WebSocket broadcast")
