import logging
import time
from functools import wraps

# This logger will now use the config from setup_logging()
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
            # logger.exception automatically includes the full Traceback
            logger.exception(f"EXCEPTION in {func.__name__}: {str(e)}")
            raise
        finally:
            elapsed_time = time.time() - start_time
            logger.info(f"FINISHED: {func.__name__} in {elapsed_time:.2f}s")
    return wrapper