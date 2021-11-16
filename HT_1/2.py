"""
Write a script to print out a set containing all the colours 
from color_list_1 which are not present in color_list_2
"""


def get_user_input(caption):
    return input(caption).replace(' ', '')


def covert_string_to_set(string):
    return set(string.split(','))


def main():
    first_values_group_string = get_user_input(
        '[<] insert first comma-separated values: ')

    second_values_group_string = get_user_input(
        '[<] insert second comma-separated values: ')

    first_set = covert_string_to_set(first_values_group_string)
    second_set = covert_string_to_set(second_values_group_string)

    print('[>] result:', first_set.difference(second_set))


if __name__ == '__main__':
    main()
