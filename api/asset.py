from fastapi import APIRouter
from ws.ws_client import switch_asset

router = APIRouter()

@router.post("/select-asset")
def select_asset(payload: dict):
    asset = payload.get("asset")
    if not asset:
        return {"error": "Missing asset"}
    
    switch_asset(asset)
    return {"message": f"Asset switched to {asset}"}
