from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.logger.logging_config import setup_logging
from app.routes.report_routes import router as report_router
from app.core.handler import register_exception_handlers
from app.db.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger = logging.getLogger("app.main") # Specific name for main logs
    
    # Connection Pool logging 
    logger.info("APIs Starting Up: Initializing Database Connection Pool")
    try:
        async with engine.connect() as conn:
           pass
        logger.info("Database Connection Pool: SUCCESS")
    except Exception as e:
        logger.error(f"Database Connection Pool: FAILED | {e}")
        
    yield  # Application runs here
    
    logger.info("APIs Shutting Down: Disposing Connection Pool")
    await engine.dispose()

app = FastAPI(
    title="Self-Pay Patients API",
    version="1.0.0",
    lifespan=lifespan
)

register_exception_handlers(app)
app.include_router(report_router)


















# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from app.routes.report_routes import router as report_router
# from app.core.handler import register_exception_handlers
# from app.db.database import engine # Import the engine to close it

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # --- Startup Logic ---
#     print("Connecting to the corporate database...")
#     # we can verify the connection here
    
#     yield  # This is where the app runs
    
#     # --- Shutdown Logic ---
#     print("Closing database connection pool...")
#     await engine.dispose()

# app = FastAPI(lifespan=lifespan)

# # Register the global exception handlers cleanly
# register_exception_handlers(app)

# app.include_router(report_router)