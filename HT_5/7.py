"""
Реалізуйте генератор, який приймає на вхід будь-яку ітерабельну послідовність (рядок, список, кортеж) 
і повертає генератор, який буде вертати значення з цієї послідовності, 
при цьому, якщо було повернено останній елемент із послідовності - ітерація починається знову.
"""


def generator(iterable_object):
    index = 0

    while True:
        if index == len(iterable_object):
            index = 0

        yield iterable_object[index]

        index +=1 


def main():
    g = generator('abc')

    for _ in range(8):
        print(next(g))


if __name__ == '__main__':
    main()