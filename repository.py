import contextlib
import dataclasses
from datetime import datetime
from typing import Callable, Tuple
import collections

Count = collections.namedtuple("Count", ["count", "updated_ts"])


@dataclasses.dataclass
class Count:
    count: int
    _updated_ts: str

    @property
    def updated_date(self):
        return datetime.strptime(self._updated_ts, "%Y-%m-%d").date()

class CountRepository:
    def __init__(self, db_connection: Callable):
        self.db_connection = db_connection
        self.select_query = """
            SELECT count, updated_ts 
            FROM current_count 
            WHERE id = 0;
        """
        self.update_query = """
            UPDATE current_count 
            SET count = :count,
                updated_ts = :updated_ts
            WHERE id = 0 
            RETURNING count;
        """

    @contextlib.contextmanager
    def connection_manager(self):
        conn = self.db_connection()
        try:
            yield conn
        finally:
            conn.close()

    def fetch_count(self) -> Count:
        with self.connection_manager() as conn:
            count, updated_ts, *_ = next(conn.execute(self.select_query))
            return Count(count, updated_ts)

    def update_count(self, count: int):
        with self.connection_manager() as conn:
            conn.execute(self.update_query, {"count": count, "updated_ts": datetime.utcnow().strftime("%Y-%m-%d")})
            conn.commit()
