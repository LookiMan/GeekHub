"""
Написати функцiю season, яка приймає один аргумент — номер мiсяця (вiд 1 до 12), 
яка буде повертати пору року, якiй цей мiсяць належить (зима, весна, лiто або осiнь)
"""


def season(month_number):
    if month_number in (1, 2, 3):
        return 'Зима'
    elif month_number in (4, 5, 6):
        return 'Весна'
    elif month_number in (7, 8, 9):
        return 'Літо'
    elif month_number in (10, 11, 12):
        return 'Осінь'


def main():
    month_number = int(input('[<] insert month number: '))

    if month_number in range(1, 13):
        month_name = season(month_number)

        print('[>]', month_name)
    else:
        print('[!] month number must be in the range from 1 to 12')


if __name__ == '__main__':
    main()
