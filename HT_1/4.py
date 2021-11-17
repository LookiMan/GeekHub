"""
Write a script to concatenate N strings.
"""


def main():
    strings_buffer = []

    amount_strings = int(input('[<] insert strings amount to concatenate: '))

    for index in range(1, amount_strings+1):
        strings_buffer.append(
            input(f'[<] insert string ({index}/{amount_strings}): ')
        )

    print('[>] result:', ''.join(strings_buffer))


if __name__ == '__main__':
    main()
