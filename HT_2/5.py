"""Написати скрипт, який залишить в словнику тільки пари із унікальними значеннями (дублікати значень - видалити).
"""


def main():
    input_dict = {'apple': 'red', 'banana': 'yellow',
                  'carrot': 'orange', 'tomato': 'red', 'lemon': 'yellow'}
    output_dict = dict()
    unique_values = set(input_dict.values())

    for unique_value in unique_values:
        for key in input_dict.keys():
            if input_dict[key] == unique_value:
                output_dict[key] = unique_value
                break

    print('[>] result:', output_dict)


if __name__ == '__main__':
    main()
