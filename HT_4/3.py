"""
Написати функцию < is_prime >, яка прийматиме 1 аргумент - число від 0 до 1000, 
и яка вертатиме True, якщо це число просте, и False - якщо ні.
"""


def is_prime(number):
    if number <= 1:
        return False
    else:
        for i in range(2, 1001):
            if number % i == 0:
                break
        else:
            return True

        return False


def main():
    number = int(input('[<] insert number: ').strip())

    print(f'[>] number {number} is prime: {is_prime(number)}')


if __name__ == '__main__':
    main()
