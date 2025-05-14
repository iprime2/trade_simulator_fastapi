# 📘 Trade Simulator API Documentation

This document describes the available API endpoints for the Trade Simulator backend.

Base URL (Local):
```
http://localhost:8000
```

---

## 🔁 WebSocket Feed

- **URL:** `wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/{symbol}-SWAP`
- **Example:**  
  `wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP`

- **Sample Message:**
```json
{
  "timestamp": "2025-05-04T10:39:13Z",
  "exchange": "OKX",
  "symbol": "BTC-USDT-SWAP",
  "asks": [["95445.5", "9.06"]],
  "bids": [["95445.4", "1104.23"]],
  "latency_ms": 0.0531
}
```

---

## 📥 POST /api/v1/simulate

Simulates trade execution metrics using input parameters.

- **URL:** `/api/v1/simulate`
- **Method:** `POST`
- **Request Body:**
```json
{
  "order_size_usd": 100,
  "fee_rate": 0.001,
  "order_type": "taker",
  "asset": "BTC-USDT",
  "volatility": 0.5
}
```

- **Response:**
```json
{
  "slippage": 0.12,
  "fee": 0.1,
  "market_impact": 0.25,
  "net_cost": 0.47,
  "latency_ms": 0.043,
  "maker_taker_ratio": "72% taker",
  "asset": "BTC-USDT"
}
```

---

## 🔁 GET /api/v1/live-output

Returns the most recently computed trade simulation metrics (auto-updated on each WebSocket tick).

- **URL:** `/api/v1/live-output`
- **Method:** `GET`
- **Response:** same as `/simulate`

---

## ⚙️ POST /api/v1/live-config

Updates the live simulation input parameters used during real-time tick processing.

- **URL:** `/api/v1/live-config`
- **Method:** `POST`
- **Request Body:** same as `/simulate`
- **Response:**
```json
{ "message": "Live config updated" }
```

---

## 📡 GET /api/v1/tick

Returns the most recent Level-2 orderbook tick received from the WebSocket stream.

- **URL:** `/api/v1/tick`
- **Method:** `GET`
- **Response Example:**
```json
{
  "timestamp": "2025-05-04T10:39:13Z",
  "best_bid": 95445.4,
  "best_ask": 95445.5,
  "mid_price": 95445.45,
  "latency_ms": 0.0423
}
```

- **Use Cases:**
  - Display real-time market tick data
  - Feed latency chart components
  - Sync tick visuals with current simulation metrics

---

## ✅ Response Field Descriptions

| Field               | Type    | Description                                |
|--------------------|---------|--------------------------------------------|
| `slippage`         | float   | Estimated price deviation due to order size |
| `fee`              | float   | Estimated execution fee (based on tier)    |
| `market_impact`    | float   | Expected price move from order absorption  |
| `net_cost`         | float   | Sum of slippage + fee + market impact      |
| `latency_ms`       | float   | Processing latency in milliseconds         |
| `maker_taker_ratio`| string  | Estimated execution ratio                  |
| `asset`            | string  | Selected spot trading pair (e.g., BTC-USDT)|
| `best_bid`         | float   | Best available bid price                   |
| `best_ask`         | float   | Best available ask price                   |
| `mid_price`        | float   | Average of best bid and ask                |
| `timestamp`        | string  | ISO timestamp of the latest tick           |

---

For questions or issues, please contact:  
📧 **careers@goquant.io**
