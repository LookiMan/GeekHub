"""
Написати функцію, яка приймає на вхід список і підраховує кількість однакових елементів у ньому.
"""


def main():
    input_data = ['apple', 1234, 'apple', 'cherry',
                  ('tuple', ), {'dict': 1, }, 1234, 1234, 1234, 'apple', ('tuple',), 'string', 'string']

    unique_values = []

    for value in input_data:
        if value not in unique_values:
            unique_values.append(value)

    for value in unique_values:
        amount = input_data.count(value)

        print(f'[>] {amount} value \'{value}\' in list')


if __name__ == '__main__':
    main()
