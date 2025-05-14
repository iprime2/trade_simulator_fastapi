from fastapi import FastAPI
from core import exception_handlers
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from api.simulate import router as simulate_router
from ws.ws_client import start_ws_thread
from fastapi.middleware.cors import CORSMiddleware
from api.orderbook import router as orderbook_router
from loguru import logger
import sys
from ws.ws_broadcast import router as broadcast_ws_router
from api.asset import router as asset_router
    
app = FastAPI()

# Register handlers
app.add_exception_handler(StarletteHTTPException, exception_handlers.http_exception_handler)
app.add_exception_handler(RequestValidationError, exception_handlers.validation_exception_handler)
app.add_exception_handler(Exception, exception_handlers.unhandled_exception_handler)

# Setup Loguru logger
logger.remove()
# Log to terminal
logger.add(sys.stdout, format="{time} | {level} | {message}", level="INFO")

# Log to a file
logger.add("logs/backend.log", rotation="1 MB", retention="10 days", compression="zip", level="DEBUG")

# Allow frontend domain
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "running"}

app.include_router(orderbook_router, prefix="/api/v1")
app.include_router(asset_router, prefix="/api/v1")

# app.include_router(broadcast_ws_router)

start_ws_thread()

app.include_router(simulate_router, prefix="/api/v1")