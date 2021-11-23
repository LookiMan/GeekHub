"""
Ну і традиційно -> калькулятор :) повинна бути 1 ф-цiя яка б приймала 3 аргументи 
- один з яких операцiя, яку зробити!
"""


def calculator(first_number, second_number, action):
    if action == '+':
        return first_number + second_number
    elif action == '-':
        return first_number - second_number
    if action == '*':
        return first_number * second_number
    elif action == '/':
        if second_number == 0:
            return 'division by zero is impossible'
        else:
            return first_number / second_number
    if action == '**':
        return first_number ** second_number
    elif action == '//':
        if second_number == 0:
            return 'division by zero is impossible'
        else:
            return first_number // second_number


def main():
    while True:
        try:
            first_number = int(input('[<] insert first number: ').strip())
            second_number = int(input('[<] insert second number: ').strip())
        except ValueError as error:
            print(f'[!] insert correct number. {error}')
            continue

        action = input('[<] insert action (+ - * / // **): ').strip()

        if action not in ('+', '-', '*', '/', '//', '**'):
            print('[!] insert correct action (+ - * / // **)')
            continue

        result = calculator(first_number, second_number, action)

        print(f'[>] {first_number} {action} {second_number} = {result}')


if __name__ == '__main__':
    main()
