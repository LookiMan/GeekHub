"""
Написати функцію < fibonacci >, яка приймає один аргумент і виводить всі числа Фібоначчі, 
що не перевищують його.
"""


def fibonacci(n):
    a, b = 0, 1

    for i in range(n):
        if a > n:
            break

        yield a

        a, b = b, a + b


def main():
    number = int(input('[<] insert number from calculate fibonacci: ').strip())
    data = list(fibonacci(number))

    print('[>]', data)


if __name__ == '__main__':
    main()
