"""
Написати скрипт, який отримає максимальне і мінімальне значення із словника.
"""


def main():
    dict_1 = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}

    dict_values = dict_1.values()

    print('[>] MIN:', min(dict_values))
    print('[>] MAX:', max(dict_values))


if __name__ == '__main__':
    main()
