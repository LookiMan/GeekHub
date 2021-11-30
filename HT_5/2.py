"""
Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну цифру;
   - щось своє :)
   Якщо якийсь із параментів не відповідає вимогам - породити виключення із відповідним текстом.
"""


class ValidateException(Exception):
    def __init__(self, message=None):
        self.message = message

    
    def __str__(self): 
        if self.message:
            return f'ValidateException, {self.message}'
        else:
            return 'ValidateException has been raised'


def has_digit(string):
    return any(map(str.isdigit, string))


def validate(username, password):
    if len(username) not in range(3, 50+1):
        raise ValidateException('invalid username length')
    elif len(password) < 8:
        raise ValidateException('invalid password length')
    elif not has_digit(password):
        raise ValidateException('password must have at least one digit')
    elif password in ('qwerty1234', '12345678', '00000000', '0987654321', '1password1'):
        raise ValidateException('common password')


def main():
    username = input('[<] insert username: ').strip()
    password = input('[<] insert password: ').strip()

    validate(username, password)


if __name__ == '__main__':
    main()
