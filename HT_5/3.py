"""
На основі попередньої функції створити наступний кусок кода:
а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь по правилам своєї функції) 
- як валідні, так і ні;
б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором, 
перевірить ці дані і надрукує для кожної пари значень відповідне повідомлення, наприклад:
    Name: vasya
    Password: wasd
    Status: password must have at least one digit
    -----
    Name: vasya
    Password: vasyapupkin2000
    Status: OK
P.S. Не забудьте використати блок try/except ;)
"""


class ValidateException(Exception):
    pass


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
    users = [
        ('Ivan', 'ivan1234'), 
        ('Tom', 'qwerty1234'),  
        ('Sam', 'password'), 
        ('Jess', '2345'), 
        ('Lana', 'ERROR0001')
        ]

    for username, password in users:
        print('[>] Name:', username)
        print('[>] Password:', password)

        try:
            validate(username, password)
        except ValidateException as val_exc:
            print('[!] Status:', val_exc)
        except Exception as exc:
            print('[!] Unexpected error:', exc)
        else:
            print('[>] Status: OK')


if __name__ == '__main__':
    main()
