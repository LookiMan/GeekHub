"""
Написати скрипт, який пройдеться по списку, який складається із кортежів,
і замінить для кожного кортежа останнє значення.

Список із кортежів можна захардкодити. Значення, на яке замінюється останній елемент кортежа вводиться користувачем.
Значення, введене користувачем, можна ніяк не конвертувати (залишити рядком). Кількість елементів в кортежу повинна бути різна.
"""


def main():
    input_data = [(10, 20, 40), (40, 50, 60, 70), (80, 90), (1000,)]
    required_value = input(
        '[<] insert the value you want to replace the last element of the tuple: ')

    for index in range(len(input_data)):
        item = input_data[index]

        new_list_item = list(item)
        new_list_item[-1] = required_value

        new_tuple_item = tuple(new_list_item)

        input_data[index] = new_tuple_item

    print('[>] result:', input_data)


if __name__ == '__main__':
    main()
