from fastapi import FastAPI
from app.routes.report_routes import router as report_router
from app.core.handler import register_exception_handlers

app = FastAPI()

# Register the global exception handlers cleanly
register_exception_handlers(app)

app.include_router(report_router)