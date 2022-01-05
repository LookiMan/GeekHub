"""
2. Створити клас Person, в якому буде присутнім метод __init__ який буде приймати * аргументів, 
які зберігатиме в відповідні змінні. Методи, які повинні бути в класі Person - show_age, print_name, show_all_information.
- Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть атребут profession.
"""


class Person(object):
    """

    Methods
    -------
    show_age()
    print_name()
    show_all_information()
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def show_age(self):
        print(self.kwargs.get("age"))

    def print_name(self):
        print(self.kwargs.get("name"))

    def show_all_information(self):
        print(self.kwargs)


person1 = Person(age=25, name="Ivan")
person2 = Person(age=32, name="Bob")

person1.profession = "builder"
person2.profession = "writer"
