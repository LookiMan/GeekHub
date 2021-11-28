"""
Написати функцію < square > , яка прийматиме один аргумент - сторону квадрата, 
і вертатиме 3 значення (кортеж): периметр квадрата, площа квадрата та його діагональ.
"""

import math


def square(side_size):
    p = side_size * 4
    s = side_size * side_size
    d = side_size * math.sqrt(2)

    return (p, s, d)


def main():
    size = int(input('[<] insert square side size: ').strip())
    result = square(size)

    print(f'[>] Results: p={result[0]} s={result[1]} d={result[2]}')


if __name__ == '__main__':
    main()
