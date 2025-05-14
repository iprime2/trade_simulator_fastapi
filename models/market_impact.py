from loguru import logger

class MarketImpactModel:
    def __init__(self, gamma=0.0005, eta=0.0001, N=10):
        self.gamma = gamma
        self.eta = eta
        self.N = N

    def estimate_impact(self, order_size_usd: float) -> float:
        try:
            permanent = self.gamma * order_size_usd
            temporary = self.eta * (order_size_usd ** 2) / self.N
            impact = round(permanent + temporary, 4)
            logger.debug(
                f"[IMPACT] Order: ${order_size_usd} → Permanent: {permanent:.4f}, Temporary: {temporary:.4f}, Total: {impact}"
            )
            return impact
        except Exception as e:
            logger.exception(f"[IMPACT] Failed to estimate market impact for order size ${order_size_usd}")
            return 0.0  # Fallback value
