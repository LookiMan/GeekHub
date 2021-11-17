"""
Write a script to convert decimal to hexadecimal.
"""


def main():
    raw_input = input('[<] insert comma-separated decimals: ').replace(' ', '')

    values = filter(lambda value: value.isdecimal(), raw_input.split(','))

    decimals = map(int, values)
    result = map(lambda value: hex(value)[2:], decimals)

    print('[>] result:', ', '.join(result))


if __name__ == '__main__':
    main()
