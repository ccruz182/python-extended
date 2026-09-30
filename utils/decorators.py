# utils/decorators.py
import functools
import time
import logging
from typing import Type

logger = logging.getLogger(__name__)


def retry(
    max_attempts: int = 4,
    delay: float = 1.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,)
):
    """
    Reintenta la función si lanza una excepción.

    Usage:
        @retry(max_attempts=3, delay=0.5, exceptions=(IOError, TimeoutError))
        def call_nasa_api(spacecraft_id: int): ...
    """
    def decorator(func):
        @functools.wraps(func)  # preserva nombre, docstring y firma original
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        logger.error(
                            f"[{func.__name__}] failed after "
                            f"{max_attempts} attempts — {e}"
                        )
                        raise
                    logger.warning(
                        f"[{func.__name__}] attempt {attempt} failed: {e} "
                        f"→ retrying in {delay}s"
                    )
                    time.sleep(delay)
        return wrapper
    return decorator

def log_call(func):
    """
    Loguea entrada, salida y tiempo de ejecución.

    Usage:
        @log_call
        def transform_anomaly(record: dict) -> dict: ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"[{func.__name__}] started")
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            logger.info(f"[{func.__name__}] completed in {elapsed:.3f}s")
            return result
        except Exception as e:
            elapsed = time.perf_counter() - start
            logger.error(
                f"[{func.__name__}] failed after {elapsed:.3f}s — {e}"
            )
            raise
    return wrapper
