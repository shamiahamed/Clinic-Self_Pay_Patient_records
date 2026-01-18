from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.report_routes import router as report_router
from app.core.handler import register_exception_handlers
from app.db.database import engine # Import the engine to close it

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup Logic ---
    print("Connecting to the corporate database...")
    # we can verify the connection here
    
    yield  # This is where the app runs
    
    # --- Shutdown Logic ---
    print("Closing database connection pool...")
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# Register the global exception handlers cleanly
register_exception_handlers(app)

app.include_router(report_router)