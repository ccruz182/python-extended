import logging
from utils.timer import timer
from utils.db_context import db_connection
from utils.batch_writer import batch_writer
from utils.decorators import retry, log_call

logging.basicConfig(level=logging.INFO)

DB_CONFIG = {
    'host':     'localhost',
    'port':     5432,
    'dbname':   'spacecraft_db',
    'user':     'postgres',
    'password': ''
}

@retry(max_attempts=3, delay=0.5)
@log_call
def test_1():
    print("a")


with timer("TIME_1"), batch_writer('output.jsonl', batch_size=3) as writer, db_connection(**DB_CONFIG) as conn :
    writer.append({'id': 1})

    writer.append({'id': 2})

    writer.append({'id': 3})

    cursor = conn.cursor()
    cursor.execute('SELECT id, name, class_type FROM spacecrafts LIMIT 10')
    [print(r[0], r[1], r[2]) for r in cursor.fetchall()]
    test_1()

    writer.append({'id': 4})

    writer.append({'id': 5})

