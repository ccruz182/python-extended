# utils/batch_writer.py
from contextlib import contextmanager
from typing import Generator
import json
import logging

logger = logging.getLogger(__name__)


class BatchWriter:
    """
    Acumula registros y escribe a disco cada batch_size elementos.
    """

    def __init__(self, filepath: str, batch_size: int):
        self._filepath  = filepath
        self._batch_size = batch_size
        self._batch: list = []
        self._total_written = 0

    def append(self, item: dict) -> None:
        self._batch.append(item)

        # Cada vez que el batch llega al límite → escribe y limpia
        if len(self._batch) >= self._batch_size:
            self._flush()

    def _flush(self) -> None:
        """Escribe el batch actual a disco y lo limpia."""
        if not self._batch:
            return

        with open(self._filepath, 'a') as f:
            for item in self._batch:
                f.write(json.dumps(item) + '\n')

        self._total_written += len(self._batch)
        logger.info(
            f"Wrote {len(self._batch)} records "
            f"→ total: {self._total_written}"
        )
        self._batch.clear()

    def close(self) -> None:
        """Escribe lo que quedó en el batch al cerrar."""
        self._flush()
        logger.info(f"BatchWriter closed — total written: {self._total_written}")


@contextmanager
def batch_writer(filepath: str,
                 batch_size: int = 100) -> Generator[BatchWriter, None, None]:
    writer = BatchWriter(filepath, batch_size)
    try:
        yield writer        # el 'as writer' recibe el objeto BatchWriter
    finally:
        writer.close()      # siempre cierra aunque haya excepción
