"""
Write a script to convert decimal to hexadecimal.
"""


def convert_decimal_to_hexadecimal(decimal):
    if decimal in range(1, 10):
        return '0%x' % decimal
    return '%x' % decimal


def main():
    raw_input = input('[<] insert comma-separated decimals: ').replace(' ', '')

    values = filter(lambda value: value.isdecimal(), raw_input.split(','))

    decimals = map(int, values)
    result = map(convert_decimal_to_hexadecimal, decimals)

    print('[>] result:', ', '.join(result))


if __name__ == '__main__':
    main()
