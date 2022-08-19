from server.utils.db import DB
from server.utils.db import lock_thread


class BannedDB(DB):
    def __init__(self) -> None:
        super().__init__()
        self._table = "banned"
        self._column = "user_id"

    @lock_thread
    def get_users(self) -> list[int]:
        self._bd_cursor.execute(f'SELECT {self._column} FROM {self._table}')
        records = self._bd_cursor.fetchall()
        records_listed = [record[0] for record in records]
        return records_listed

    def _get_users(self) -> list[tuple]:
        self._bd_cursor.execute(f'SELECT * FROM {self._table}')
        records = self._bd_cursor.fetchall()
        records_listed = []
        for record in records:
            records_listed.append((record[0], record[1]))
        return records_listed

    @lock_thread
    def ban(self, user_id: int, user_name: str) -> None:
        self._bd_cursor.execute(f'INSERT INTO {self._table} ({self._column}, user_name) VALUES (?, ?)', (user_id, user_name))
        self._bd.commit()
    
    @lock_thread
    def get_users_idName_list(self) -> str:
        txt = ''
        users = self._get_users()
        for user in users:
            txt += (f'{user[0]} -- {user[1]}\n')
        return txt