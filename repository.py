import contextlib
import sqlite3
from typing import Callable


class CountRepository:
    def __init__(self, db_connection: Callable):
        self.db_connection = db_connection
        self.select_query = """
            SELECT count FROM current_count WHERE id = 0;
        """
        self.update_query = """
            UPDATE current_count SET count = :count WHERE id = 0 RETURNING count;
        """

    @contextlib.contextmanager
    def connection_manager(self):
        conn = self.db_connection()
        try:
            yield conn
        finally:
            conn.close()

    def fetch_count(self) -> int:
        with self.connection_manager() as conn:
            count, = next(conn.execute(self.select_query))
            return count

    def update_count(self, count: int):
        with self.connection_manager() as conn:
            conn.execute(self.update_query, {"count": count})
            conn.commit()
