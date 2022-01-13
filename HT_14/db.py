import sqlite3


class SQLite:
    def __init__(self, filename: str) -> None:
        self._filename = filename

    def _connect(self):
        conn = sqlite3.connect(self._filename)
        return conn, conn.cursor()

    def select_banknotes(self) -> tuple:
        connection, cursor = self._connect()
        query = """SELECT * FROM banknotes"""
        result = cursor.execute(query).fetchall()
        connection.close()
        return result

    def select_user_balance(self, user_id: int) -> int:
        connection, cursor = self._connect()
        query = """SELECT `balance` FROM balances WHERE user_id=?"""
        result = cursor.execute(query, (user_id,)).fetchone()
        connection.close()
        return result[0]

    def append_user_transaction(self, user_id: int, transaction: str) -> None:
        connection, cursor = self._connect()
        query = """INSERT INTO transactions VALUES (?, ?)"""
        cursor.execute(query, (user_id, transaction))
        connection.commit()
        connection.close()

    def update_user_balance(self, user_id: int, balance: int) -> None:
        connection, cursor = self._connect()
        query = """UPDATE balances SET balance=? WHERE user_id=?"""
        cursor.execute(query, (balance, user_id))
        connection.commit()
        connection.close()

    def update_banknotes(self, banknotes: dict) -> None:
        connection, cursor = self._connect()
        query = """UPDATE banknotes SET amount=? WHERE nominal=?"""
        cursor.executemany(query, [(value, key)
                           for key, value in banknotes.items()])
        connection.commit()
        connection.close()

    def is_incasator(self, user_id: int) -> bool:
        connection, cursor = self._connect()
        query = """SELECT COUNT(*) FROM users WHERE id=? AND is_incasator=1"""
        result = cursor.execute(query, (user_id,)).fetchone()
        connection.close()
        return result[0] == 1

    def is_user_exists(self, username: str, password: str) -> bool:
        connection, cursor = self._connect()
        query = """SELECT `id` FROM users WHERE username=? AND password=?"""
        result = cursor.execute(query, (username, password)).fetchone()
        connection.close()
        return result[0] if result else False
