from fastapi import APIRouter
from ws.ws_client import latest_orderbook

router = APIRouter()

@router.get("/tick")
def get_latest_tick():
    return latest_orderbook
