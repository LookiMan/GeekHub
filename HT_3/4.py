"""
Створiть 3 рiзних функцiї (на ваш вибiр). Кожна з цих функцiй повинна повертати якийсь результат. 
Також створiть четверу ф-цiю, яка в тiлi викликає 3 попереднi, 
обробляє повернутий ними результат та також повертає результат. 
Таким чином ми будемо викликати 1 функцiю, а вона в своєму тiлi ще 3
"""

from random import randint


def get_random_number():
    return randint(-111_111_111, 999_999_999)


def square(number):
    return number ** 2


def formated_result(number, square_number):
    return f'Square of number {number} is {square_number}'


def main():
    number = get_random_number()
    square_number = square(number)
    result = formated_result(number, square_number)

    print('[>]', result)


if __name__ == '__main__':
    main()
