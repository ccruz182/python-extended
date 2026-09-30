# utils/db_context.py
from contextlib import contextmanager
from typing import Generator
import psycopg2
import logging

logger = logging.getLogger(__name__)


@contextmanager
def db_connection(host: str, port: int, dbname: str,
                  user: str, password: str) -> Generator:
    """
    Context manager para conexión a PostgreSQL.
    Garantiza cierre de conexión aunque haya excepción.
    
    Usage:
        with db_connection(**config) as conn:
            conn.execute('SELECT * FROM spacecrafts')
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        logger.info(f"DB connection opened → {dbname}")
        yield conn                     # el 'as conn' recibe esto
        conn.commit()                  # commit si todo salió bien
    except Exception as e:
        if conn:
            conn.rollback()            # rollback si algo falló
        logger.error(f"DB error: {e}")
        raise
    finally:
        if conn:
            conn.close()               # siempre cierra
            logger.info("DB connection closed")
