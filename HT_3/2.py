"""
Користувачем вводиться початковий і кінцевий рік. 
Створити цикл, який виведе всі високосні роки в цьому проміжку (границі включно).
"""


def is_leap_year(year):
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return True
    else:
        return False


def main():
    start_year = int(input('[<] inser start year: '))
    end_year = int(input('[<] inser end year: '))

    for year in range(start_year, end_year+1):
        if is_leap_year(year):
            print(f'[>] {year} is leap year!')


if __name__ == '__main__':
    main()
