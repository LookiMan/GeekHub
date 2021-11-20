"""
Написати скрипт, який залишить в словнику тільки пари із унікальними значеннями (дублікати значень - видалити).
"""


def main():
    input_dict = {'apple': ('red',), 'banana': 'yellow',
                  'carrot': ['orange', ], 'tomato': ('red',), 'lemon': 'yellow'}

    unique_values = list()
    output_dict = dict()

    for key in input_dict.keys():
        value = input_dict[key]

        if value not in unique_values:
            unique_values.append(value)
            output_dict[key] = value

    print('[>] result:', output_dict)


if __name__ == '__main__':
    main()
