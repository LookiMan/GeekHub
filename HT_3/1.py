"""
Створити цикл від 0 до ... (вводиться користувачем). 
В циклі створити умову, яка буде виводити поточне значення, 
якщо остача від ділення на 17 дорівнює 0.
"""


def main():
    max_range_value = int(input('[<] insert random integer: '))

    for i in range(max_range_value):
        if not i % 17:
            print(f'[>] {i}')


if __name__ == '__main__':
    main()
