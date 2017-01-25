import os


def get_absolute_path_of_file_parent_directory(file_name: str) -> str:
    return os.sep.join(__file__.split(os.sep)[:-1])


def get_valid_input(input_str: str, valid_options: tuple):
    while True:
        response = input(input_str)
        if response in valid_options:
            return response
        print('Invalid option')


def print_friends(friends, action):
    if not friends:
        print('There are no friends to {}.'.format(action))
        return

    print('Friends:')
    for i, friend in enumerate(friends):
        print('{0}. {1}'.
              format(i + 1, friend.full_name))
