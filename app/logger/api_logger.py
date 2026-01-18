import os, logging, time
# Decorator to log function execution time
from functools import wraps
from pathlib import Path

# logger for error , info and time logging
# Define base project directory (use absolute path or dynamic relative path)
base_dir = Path(__file__).resolve().parent

# Define logs subdirectory inside your project
log_dir = os.path.join(base_dir, "logs")
os.makedirs(log_dir, exist_ok=True)  # Create it if not exists

logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def log_execution(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"STARTED: {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(f"EXCEPTION in {func.__name__}: {e}")
            raise
        finally:
            elapsed_time = time.time() - start_time
            logger.info(f"FINISHED: {func.__name__} in {elapsed_time:.2f}s")
    return wrapper
