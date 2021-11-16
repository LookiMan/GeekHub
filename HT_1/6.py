"""
Write a script to check whether a specified value is contained in a group of values.
"""


def get_user_input(caption):
    return input(caption).replace(' ', '')


def covert_string_to_tuple(string):
    return tuple(string.split(','))


def main():
    first_values_group_string = get_user_input(
        '[<] insert comma-separated group of values: ')

    specified_value = get_user_input(
        '[<] insert specified value: ')

    values_group = covert_string_to_tuple(first_values_group_string)

    print('[>] result:', specified_value in values_group)


if __name__ == '__main__':
    main()
