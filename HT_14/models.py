
from typing import NamedTuple

from storage import Storage


class DecomposerStatuses(NamedTuple):
    success: int
    fail: int


class Person(object):
    def __init__(self, user_id: int, name: str, storage: Storage) -> None:
        self.user_id = user_id
        self.name = name
        self.storage = storage

    def username(self) -> str:
        return self.name

    def is_incasator(self) -> bool:
        raise BaseException("Method \'is_incasator\' not implemented")

    def balance(self) -> int:
        return self.storage.load_user_balance(self.user_id)

    def save_balance(self, balance: int) -> None:
        self.storage.save_user_balance(self.user_id, balance)

    def append_user_transaction(self, transaction: str) -> None:
        self.storage.append_user_transactions(self.user_id, transaction)


class User(Person):
    def __init__(self, user_id: int, name: str, storage: Storage) -> None:
        super().__init__(user_id, name, storage)

    def is_incasator(self):
        return False


class Incasator(Person):
    def __init__(self, user_id: int, name: str, storage: Storage) -> None:
        super().__init__(user_id, name, storage)

    def is_incasator(self):
        return True
