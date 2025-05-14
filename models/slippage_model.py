import numpy as np
from sklearn.linear_model import LinearRegression
from loguru import logger

class SlippageEstimator:
    def __init__(self):
        self.model = LinearRegression()
        try:
            self._train_mock_model()
            logger.info("[SLIPPAGE] Model trained with simulated data")
        except Exception as e:
            logger.exception("[SLIPPAGE] Failed to train model")

    def _train_mock_model(self):
        X = np.random.uniform(10, 1000, size=(1000, 1))
        y = X * np.random.uniform(0.001, 0.003) + np.random.normal(0, 0.05, size=(1000, 1))
        self.model.fit(X, y)

    def predict_slippage(self, order_size_usd: float) -> float:
        try:
            predicted = self.model.predict([[order_size_usd]])[0][0]
            logger.debug(f"[SLIPPAGE] Predicted slippage for ${order_size_usd}: {predicted:.4f}")
            return float(predicted)
        except Exception as e:
            logger.exception(f"[SLIPPAGE] Failed to predict slippage for ${order_size_usd}")
            return 0.0  # Fallback to avoid crashing downstream
