"""
Write a script which accepts a sequence of comma-separated numbers 
from user and generate a list and a tuple with those numbers.
"""


def main():
    raw_string = input('[<] insert values: ').replace(' ', '')

    numbers_list = raw_string.split(',')
    numbers_tuple = tuple(numbers_list)

    print(numbers_list)
    print(numbers_tuple)


if __name__ == '__main__':
    main()
