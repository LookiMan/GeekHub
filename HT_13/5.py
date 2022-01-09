"""
5. Створіть за допомогою класів та продемонструйте свою реалізацію шкільної бібліотеки(включіть фантазію).
"""

from typing import Optional


class Book(object):
    def __init__(self, name: str, amount_pages: int, author: str) -> None:
        self._name = name
        self._amount_pages = amount_pages
        self._author = author

    def __str__(self) -> str:
        return (
            f"Book: {self._name}, author: {self._author}, pages: {self._amount_pages}"
        )

    def name(self) -> str:
        return self._name

    def amount_pages(self) -> int:
        return self._amount_pages

    def author(self) -> str:
        return self._author


class Library(object):
    def __init__(self) -> None:
        self._books = []

    def _pop_book_by_name(self, name: str) -> Optional[Book]:
        for index in range(len(self._books)):
            if self._books[index].name() == name:
                return self._books.pop(index)

    def _pop_book_by_author(self, author: str) -> Optional[Book]:
        for index in range(len(self._books)):
            if self._books[index].author() == author:
                return self._books.pop(index)

    def authors_list(self) -> list:
        return [book.author() for book in self._books]

    def book_names_list(self) -> list:
        return [book.name() for book in self._books]

    def is_has_author(self, author: str) -> bool:
        return author in self.authors_list()

    def is_has_book_name(self, name: str) -> bool:
        return name in self.book_names_list()

    def append_book(self, book: Book) -> None:
        self._books.append(book)

    def get_book_by_name(self, name: str) -> Optional[Book]:
        if self.is_has_book_name(name):
            return self._pop_book_by_name(name)

    def get_book_by_author(self, author: str) -> Optional[Book]:
        if self.is_has_author(author):
            return self._pop_book_by_author(author)

    def get_amount_books(self) -> int:
        return len(self._books)


def main() -> None:
    lib = Library()

    lib.append_book(Book("Буквар", 50, "Іван Федорович"))
    lib.append_book(Book("Джерельце", 60, "Петро Петров"))

    history1 = Book("Історія", 452, "Федір Миколайович")
    history2 = Book("Історія", 452, "Федір Миколайович")
    history3 = Book("Історія", 452, "Федір Миколайович")

    lib.append_book(history1)
    lib.append_book(history2)
    lib.append_book(history3)

    math1 = Book("Математика", 452, "Федір Миколайович")
    math2 = Book("Математика", 452, "Федір Миколайович")

    lib.append_book(math1)
    lib.append_book(math2)

    print("authors list:", lib.authors_list())
    print("book names list:", lib.book_names_list())

    print("amount books:", lib.get_amount_books())
    print(lib.get_book_by_name("Історія"))
    print("amount books:", lib.get_amount_books())
    print(lib.get_book_by_author("Петро Петров"))
    print("amount books:", lib.get_amount_books())


if __name__ == "__main__":
    main()
