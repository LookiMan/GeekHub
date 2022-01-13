import db


class Storage(object):
    def __init__(self, database: db.SQLite) -> None:
        self.db = database

    def load_banknotes(self) -> dict:
        banknotes = {}

        for item in self.db.select_banknotes():
            banknotes[item[0]] = item[1]

        return banknotes

    def save_banknotes(self, banknotes: dict) -> None:
        self.db.update_banknotes(banknotes)

    def load_user_balance(self, user_id: int) -> int:
        return self.db.select_user_balance(user_id)

    def save_user_balance(self, user_id: int, balance: int) -> None:
        self.db.update_user_balance(user_id, balance)

    def append_user_transactions(self, user_id: int, transaction: str) -> None:
        self.db.append_user_transaction(user_id, transaction)

    def is_incasator(self, user_id: int) -> bool:
        return self.db.is_incasator(user_id)

    def is_user_exists(self, username: str, password: str) -> bool:
        return self.db.is_user_exists(username, password)
