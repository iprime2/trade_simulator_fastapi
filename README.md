# 🚀 Trade Simulator Backend Setup Guide

This guide helps you set up and run the Python FastAPI backend for the Trade Simulator on **Windows**, **macOS**, and **Linux**.

---

## 🧰 Prerequisites

- Python 3.10+ installed
- `pip` package manager
- Git (optional)

---

## 🗂 Clone the Project (if applicable)

```bash
git clone https://github.com/your-username/trade-simulator-backend.git
cd trade-simulator-backend
```

---

## ✅ 1. Create Virtual Environment

### 🪟 Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 🍎 macOS / 🐧 Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> Make sure your terminal shows the virtual environment is activated (you'll see `(venv)` before the prompt)

---

## 🚀 3. Start the Backend Server

```bash
uvicorn main:app --reload
```

This will start the FastAPI server at:

```
http://127.0.0.1:8000
```

You can test the API at:

```
http://127.0.0.1:8000/docs
```

(Interactive Swagger UI)

---

## 🧼 4. Deactivate Virtual Environment (Optional)

```bash
deactivate
```

---

## 🧠 Notes

- Ensure your Python version is compatible with all packages in `requirements.txt`
- Use a VPN if accessing live data from OKX
- If port 8000 is in use, run:  
  ```bash
  uvicorn main:app --reload --port 8001
  ```

---

## 📚 API Documentation

For detailed information on available API endpoints, request/response formats, and usage examples, see:

👉 [View Full API Docs](./api-docs.md)

---
