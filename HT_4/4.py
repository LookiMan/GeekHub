"""
4. Написати функцію < prime_list >, яка прийматиме 2 аргументи - початок і кінець діапазона, 
і вертатиме список простих чисел всередині цього діапазона.
"""


def is_prime(number):
    if number <= 1:
        return False
    else:
        for i in range(2, number):
            if number % i == 0:
                break
        else:
            return True

        return False


def prime_list(start_number, end_number):
    prime_numbers = []

    for number in range(start_number, end_number):
        if is_prime(number):
            prime_numbers.append(number)

    return prime_numbers


def main():
    start_number = int(input('[<] insert start number: ').strip())
    end_number = int(input('[<] insert end number: ').strip())

    prime_numbers = prime_list(start_number, end_number)

    print('[>]', prime_numbers)


if __name__ == '__main__':
    main()
