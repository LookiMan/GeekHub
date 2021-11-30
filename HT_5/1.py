"""
Створіть функцію, всередині якої будуть записано список із п'яти користувачів (ім'я та пароль).
Функція повинна приймати три аргументи: 
два - обов'язкових (<username> та <password>) і третій - необов'язковий параметр <silent> (значення за замовчуванням - <False>).
Логіка наступна:
якщо введено коректну пару ім'я/пароль - вертається <True>;
якщо введено неправильну пару ім'я/пароль і <silent> == <True> - функція вертає <False>, 
інакше (<silent> == <False>) - породжується виключення LoginException
"""


class LoginException(Exception):
    pass


def login(username, password, silent=False):
    users = [
            ('Ivan', 'ivan1234'),
            ('Tom', 'qwerty'), 
            ('Sam', 'lol1'), 
            ('Jess', '2345'), 
            ('Lana', 'L0001'),
        ]

    if (username, password) in users:
        return True
    elif silent == True:
        return False
    else:
        raise LoginException('wrong login or password')


def main():
    username = input('[<] insert username: ').strip()
    password = input('[<] insert password: ').strip()

    is_authorized = login(username, password)

    print('[>] Authorized:', is_authorized)


if __name__ == '__main__':
    main()
