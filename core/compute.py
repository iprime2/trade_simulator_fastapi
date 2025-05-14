import time
from loguru import logger
from models.slippage_model import SlippageEstimator
from models.fees import FeeCalculator
from models.market_impact import MarketImpactModel
from fastapi import HTTPException
import math

# Initialize models once
slippage_model = SlippageEstimator()
fee_model = FeeCalculator()
impact_model = MarketImpactModel()

def compute_trade_metrics(
    order_size_usd: float,
    fee_rate: float = None,
    order_type: str = "taker",
    asset: str = "BTC-USDT",
    volatility: float = 0.5
) -> dict:
    logger.info(f"[COMPUTE] Simulating {asset} | Qty: ${order_size_usd} | Vol: {volatility} | Type: {order_type}")

    start_time = time.perf_counter()

    try:
        slippage = slippage_model.predict_slippage(order_size_usd) * (1 + volatility)
        fee = fee_model.calculate_fee(order_size_usd, fee_rate, order_type)
        impact = impact_model.estimate_impact(order_size_usd) * (1 + volatility)
        maker_taker_ratio = estimate_maker_taker_ratio(order_size_usd, volatility)

        net_cost = round(slippage + fee + impact, 4)
        latency_ms = round((time.perf_counter() - start_time) * 1000, 4)

        result = {
            "slippage": round(slippage, 4),
            "fee": fee,
            "market_impact": round(impact, 4),
            "net_cost": net_cost,
            "latency_ms": latency_ms,
            "maker_taker_ratio": maker_taker_ratio,
            "asset": asset 
        }

        logger.debug(f"[COMPUTE] Net Cost: ${net_cost}, Latency: {latency_ms} ms")
        return result

    except Exception as e:
        logger.exception("[COMPUTE] Failed to calculate trade metrics")
        raise HTTPException(status_code=500, detail="Trade simulation failed")


def estimate_maker_taker_ratio(order_size_usd: float, volatility: float) -> str:
    # Logistic function based on order size and volatility
    x = 0.02 * order_size_usd + 10 * volatility - 5
    probability_taker = 1 / (1 + math.exp(-x))  # sigmoid
    percentage = round(probability_taker * 100, 1)

    if percentage > 75:
        label = f"{percentage}% taker"
    elif percentage < 25:
        label = f"{100 - percentage}% maker"
    else:
        label = f"{100 - percentage}% maker / {percentage}% taker"

    return label
