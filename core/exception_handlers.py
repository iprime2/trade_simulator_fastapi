from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"[HTTP ERROR] {exc.status_code} {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"[VALIDATION ERROR] {exc.errors()} - {request.url}")
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request", "details": exc.errors()}
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"[UNHANDLED EXCEPTION] {exc} - {request.url}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
