"""
Написати функцію < bank > , яка працює за наступною логікою: 
користувач робить вклад у розмірі < a > одиниць строком на < years > років під < percents > відсотків 
(кожен рік сума вкладу збільшується на цей відсоток, 
ці гроші додаються до суми вкладу і в наступному році на них також нараховуються відсотки). 
Параметр < percents > є необов'язковим і має значення по замовчуванню < 10 > (10%). 
Функція повинна принтануть і вернуть суму, яка буде на рахунку.
"""


def bank(contribution_size, years, percents=10):
    print('[>]', contribution_size * (1+percents/100)**years)


def main():
    contribution_size = int(input('[<] contribution size: ').strip())
    years = int(input('[<] years: ').strip())

    bank(contribution_size, years)


if __name__ == '__main__':
    main()
