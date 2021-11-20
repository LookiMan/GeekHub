"""
Написати скрипт, який об'єднає три словника в самий перший. Оновлюється тільки перший словник. 
"""


def main():
    dict_1 = {1: 10, 2: 20}
    dict_2 = {3: 30, 4: 40}
    dict_3 = {5: 50, 6: 60}

    dict_1.update(dict_2)
    dict_1.update(dict_3)

    print('[>] result:', dict_1)


if __name__ == '__main__':
    main()
