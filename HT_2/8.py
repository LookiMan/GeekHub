"""
Написати скрипт, який отримує від користувача позитивне ціле число і створює словник,
з ключами від 0 до введеного числа, а значення для цих ключів - це квадрат ключа.
"""


def square(integer):
    return integer * integer


def main():
    output_data = dict()

    integer = int(input('[<] insert integer: '))

    for value in range(integer+1):
        output_data[value] = square(value)

    print('[>] result:', output_data)


if __name__ == '__main__':
    main()
