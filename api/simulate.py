from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.compute import compute_trade_metrics
from loguru import logger
from ws.ws_client import latest_output, user_sim_config 

router = APIRouter()


class SimulationInput(BaseModel):
    order_size_usd: float
    fee_rate: float | None = None
    order_type: str = "taker"
    asset: str
    volatility: float


class LiveConfigInput(SimulationInput):
    pass

# Output schema
class SimulationResult(BaseModel):
    slippage: float
    fee: float
    market_impact: float
    net_cost: float
    latency_ms: float
    maker_taker_ratio: str
    asset: str

@router.post("/simulate", response_model=SimulationResult)
def simulate(input: SimulationInput):
    try:
        logger.info(f"Simulating trade: {input}")
        result = compute_trade_metrics(
            order_size_usd=input.order_size_usd,
            fee_rate=input.fee_rate,
            order_type=input.order_type,
            asset=input.asset,
            volatility=input.volatility
        )
        return result
    except Exception as e:
        logger.exception("Simulation failed")
        raise HTTPException(status_code=500, detail="Simulation error")


@router.post("/live-config")
def set_live_config(config: LiveConfigInput):
    user_sim_config.update(config.dict())
    return {"message": "Live config updated"}


@router.get("/live-output", response_model=SimulationResult)
def get_live_metrics():
    return latest_output  

