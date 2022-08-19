from server.utils.db import DB
from server.utils.db import lock_thread


class BannedDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self._table = "banned"
        self._column = "id"

    @lock_thread
    def get_users(self) -> list[int]:
        info = self._bd_cursor.execute(f'SELECT {self._column} FROM {self._table}')
        records = self._bd_cursor.fetchall()
        records_listed = [record[0] for record in records]
        return records_listed