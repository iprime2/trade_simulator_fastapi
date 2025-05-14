# ws_client.py

import json
import time
import threading
import asyncio
from websocket import WebSocketApp
from core.compute import compute_trade_metrics
from loguru import logger

# Shared state
latest_orderbook = {}
selected_asset = "BTC-USDT"
ws: WebSocketApp = None
ws_thread: threading.Thread = None
ws_stop_event = threading.Event()

latest_output = {}
user_sim_config = {
    "order_size_usd": 100,
    "fee_rate": None,
    "order_type": "taker",
    "asset": "BTC-USDT",
    "volatility": 0.5
}


def on_message(ws, message):
    try:
        start = time.perf_counter()
        data = json.loads(message)

        bids = data.get("bids", [])
        asks = data.get("asks", [])
        timestamp = data.get("timestamp", "")

        if bids and asks:
            best_bid = float(bids[0][0])
            best_ask = float(asks[0][0])
            mid_price = (best_bid + best_ask) / 2

            latest_orderbook.update({
                "timestamp": timestamp,
                "best_bid": best_bid,
                "best_ask": best_ask,
                "mid_price": mid_price,
            })

        latency_ms = (time.perf_counter() - start) * 1000
        latest_orderbook["latency_ms"] = round(latency_ms, 4)
        
        latest_output.update(
            compute_trade_metrics(
                order_size_usd=user_sim_config["order_size_usd"],
                fee_rate=user_sim_config["fee_rate"],
                order_type=user_sim_config["order_type"],
                asset=user_sim_config["asset"],
                volatility=user_sim_config["volatility"]
            )
        )

        logger.info(
            f"[TICK] {selected_asset} | Bid: {best_bid:.2f}, Ask: {best_ask:.2f}, Mid: {mid_price:.2f} | Latency: {latency_ms:.4f} ms"
        )
    except Exception:
        logger.exception("[WS] Failed to process message")


def on_error(ws, error):
    logger.error(f"[WS] Error: {error}")


def on_close(ws, code, msg):
    logger.warning(f"[WS] Closed | Code: {code} | Reason: {msg}")


def on_open(ws):
    logger.info(f"[WS] Connection opened for {selected_asset}")


def run_ws():
    global ws
    url = f"wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/{selected_asset}-SWAP"
    logger.info(f"[WS] Connecting to {url}")

    ws = WebSocketApp(
        url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

    # Blocking loop
    while not ws_stop_event.is_set():
        try:
            ws.run_forever()
        except Exception:
            logger.exception("[WS] Reconnect failed")
        time.sleep(1)


def start_ws_thread():
    global ws_thread, ws_stop_event

    if ws_thread and ws_thread.is_alive():
        logger.info("[WS] Existing thread found, shutting down...")
        ws_stop_event.set()
        ws_thread.join()

    ws_stop_event.clear()
    ws_thread = threading.Thread(target=run_ws, daemon=True)
    ws_thread.start()
    logger.info("[WS] WebSocket thread started")


def switch_asset(new_asset: str):
    global selected_asset
    if new_asset == selected_asset:
        logger.info(f"[WS] Already subscribed to {new_asset}")
        return

    logger.info(f"[WS] Switching asset from {selected_asset} to {new_asset}")
    selected_asset = new_asset
    start_ws_thread()
