from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exception import DatabaseException, ValidationException

def register_exception_handlers(app):
    @app.exception_handler(ValidationException)
    async def validation_exception_handler(request: Request, exc: ValidationException):
        return JSONResponse(
            status_code=400,
            content={"status": False, "message": exc.message, "error_type": "ValidationError"},
        )

    @app.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exc: DatabaseException):
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": "A database error occurred", "details": exc.message},
        )