from loguru import logger

class FeeCalculator:
    def __init__(self):
        self.default_fees = {
            "maker": 0.0002,  # 0.02%
            "taker": 0.001,   # 0.1%
        }

    def calculate_fee(self, order_size_usd: float, fee_rate: float = None, order_type: str = "taker") -> float:
        try:
            rate = fee_rate if fee_rate is not None else self.default_fees.get(order_type, 0.001)
            fee = round(order_size_usd * rate, 4)
            logger.debug(f"[FEE] Order: ${order_size_usd}, Type: {order_type}, Rate: {rate} → Fee: ${fee}")
            return fee
        except Exception as e:
            logger.exception(f"[FEE] Failed to calculate fee for order size ${order_size_usd}, type: {order_type}")
            return 0.0  # Fallback fee
