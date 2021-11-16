"""
Write a script to sum of the first n positive integers.
"""


def main():
    raw_input = input('[<] insert integer: ').strip()

    if raw_input.isdigit():
        n = int(raw_input)

        print('[>] result: %i' % sum(range(0, n+1)))
    else:
        print('[!] insert integer!')


if __name__ == '__main__':
    main()
