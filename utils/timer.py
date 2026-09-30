# utils/timer.py
from contextlib import contextmanager
from typing import Generator
import time
import logging

logger = logging.getLogger(__name__)


@contextmanager
def timer(name: str) -> Generator[None, None, None]:
    """
    Context manager que mide el tiempo de ejecución de un bloque.
    
    Usage:
        with timer("read anomalies"):
            rows = list(read_anomalies('anomalies.jsonl'))
    """
    start = time.perf_counter()
    try:
        yield                          # pausa aquí, ejecuta el bloque with
    except Exception as e:
        elapsed = time.perf_counter() - start
        logger.error(f"[{name}] failed after {elapsed:.3f}s — {e}")
        raise                          # propaga la excepción
    else:
        elapsed = time.perf_counter() - start
        logger.info(f"[{name}] completed in {elapsed:.3f}s")
