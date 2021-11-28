"""
Вводиться число. Якщо це число додатне, знайти його квадрат, 
якщо від'ємне, збільшити його на 100, якщо дорівнює 0, не змінювати.
"""


def main():
    number = int(input('[<] insert randon number: ').strip())

    if number > 0:
        print('[>]', number ** 2)
    elif number == 0:
        print('[>]', number)
    else:
        print('[>]', number+100)


if __name__ == '__main__':
    main()
