from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.app_module import injector
from app.ports.logging import LoggerServicePort

logger = injector.get(LoggerServicePort)


def register_exception_handlers_from_config(app: FastAPI, exception_config: dict):
    for exc_type, config in exception_config.items():
        status_code = config.get("status_code", 500)
        response_key = config.get("response_key", "detail")

        @app.exception_handler(exc_type)
        async def custom_exception_handler(request, exc):
            # Log the exception
            logger.error(f"Exception occurred: {exc}")
            # Log the request details
            logger.error(f"Request details: {request.method} {request.url}")
            return JSONResponse(
                status_code=status_code,
                content={response_key: str(exc)},
            )
