"""
Написати скрипт, який видалить пусті елементи із списка.
"""


def main():
    input_data = [(), (), ('',), ('a', 'b'), {},
                  ('a', 'b', 'c'), ('d'), '', []]

    input_data = list(filter(lambda v: len(v) > 0, input_data))

    print('[>] result:', input_data)


if __name__ == '__main__':
    main()
