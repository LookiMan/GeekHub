"""
Маємо рядок --> "f98neroi4nr0c3n30irn03ien3c0rfekdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p465jnpoj35po6j345" 

Створіть ф-цiю, яка буде отримувати рядки на зразок цього, яка оброблює наступні випадки:
- якщо довжина рядка в діапазонi 30-50 -> прiнтує довжину, кiлькiсть букв та цифр
- якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр (лише з буквами)
- якщо довжина бульше 50 - > ваша фантазiя
"""
import re


def select_all_numbers(string):
    return re.findall(r'\d', string)


def select_all_letters(string):
    return re.findall(r'\w', string)


# без використання re

def select_all_numbers(string):
    return [v for v in string if v.isdigit()]


def select_all_letters(string):
    return [v for v in string if v.isalpha()]


def calculate_sum_numbers_in_string(string):
    raw_numbers_list = select_all_numbers(string)
    numbers_list = list(map(int, raw_numbers_list))

    return sum(numbers_list)


def main():
    user_input = input('[<] insert random text: ').strip()
    len_user_input = len(user_input)

    if len_user_input in range(30, 50):
        print('[>] len:', len_user_input)
        print('[>] amount letters:', len(select_all_letters(user_input)))
        print('[>] amount numbers:', len(select_all_numbers(user_input)))
    elif len_user_input < 30:
        print('[>] sum:', calculate_sum_numbers_in_string(user_input))
        print('[>] letters:', ''.join(select_all_letters(user_input)))
    elif len_user_input > 50:
        print('[>] unique letters:', set(select_all_letters(user_input)))
        print('[>] unique numbers:', set(select_all_numbers(user_input)))


if __name__ == '__main__':
    main()
