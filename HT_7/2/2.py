"""
2. Написати функцію, яка приймає два параметри: ім'я файлу та кількість символів.
На екран повинен вивестись список із трьома блоками - символи з початку, із середини та з кінця файлу.
Кількість символів в блоках - та, яка введена в другому параметрі.
Придумайте самі, як обробляти помилку, наприклад, коли кількість символів більша, ніж є в файлі
(наприклад, файл із двох символів і треба вивести по одному символу, то що виводити на місці середнього блоку символів?)
В репозиторій додайте і ті файли, по яким робили тести.
Як визначати середину файлу(з якої брать необхідні символи) - кількість символів поділити навпіл, 
а отримане "вікно" символів відцентрувати щодо середини файла і взяти необхідну кількість. 
В разі необхідності заокруглення одного чи обох параметрів - дивіться на свій розсуд.
Наприклад:
    █ █ █ ░ ░ ░ ░ ░ █ █ █ ░ ░ ░ ░ ░ █ █ █ - правильно
    ⏫ центр
    █ █ █ ░ ░ ░ ░ ░ ░ █ █ █ ░ ░ ░ ░ █ █ █ - неправильно
    ⏫ центр
"""

import os


def read_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f'[!] файл під назвою \'{filename}\' не існує')
    else:
        with open(filename) as file:
            return file.read()


def get_start(data, number_of_characters):
    return data[:number_of_characters]


def get_middle(data, number_of_characters):
    data = data[number_of_characters:-number_of_characters]

    center = len(data) // 2
    half_char = number_of_characters // 2

    return data[center - half_char: center + number_of_characters-1]


def get_end(data, number_of_characters):
    return data[-number_of_characters:]


def main():
    filename = input('[<] ім\'я файла: ').strip()
    number_of_characters = int(input('[<] кількість символів: ').strip())

    data = read_file(filename)

    if number_of_characters > len(data):
        raise Exception('Кількість символів більша ніж довдина файлу')

    output = [
        get_start(data, number_of_characters),
        get_middle(data, number_of_characters),
        get_end(data, number_of_characters),
    ]

    print('[>]', output)


if __name__ == '__main__':
    main()
