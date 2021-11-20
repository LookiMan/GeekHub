"""
Написати скрипт, який об'єднає три словника в новий. Початкові словники не повинні змінитись.
"""


def main():
    dict_1 = {1: 10, 2: 20}
    dict_2 = {3: 30, 4: 40}
    dict_3 = {5: 50, 6: 60}

    new_dict = dict()
    new_dict.update(dict_1)
    new_dict.update(dict_2)
    new_dict.update(dict_3)

    print('[>] result:', new_dict)


if __name__ == '__main__':
    main()
