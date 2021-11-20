"""
Написати скрипт, який конкатенує всі елементи в списку і виведе їх на екран.
Елементами списку повинні бути як рядки, так і числа.
"""


def main():
    raw_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']

    processed_data = map(str, raw_data)

    print('[>] result:', ''.join(processed_data))


if __name__ == '__main__':
    main()
