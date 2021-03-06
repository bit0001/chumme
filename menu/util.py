def get_valid_input(input_str: str,
                    valid_options: tuple,
                    invalid_option_message: str='Invalid option') -> str:
    while True:
        response = input(input_str)
        if response in valid_options:
            return response
        print(invalid_option_message)


def print_friends(friends, action):
    if not friends:
        print('There are no friends to {}.'.format(action))
        return

    print('Friends:')
    for i, friend in enumerate(friends):
        print('{0}. {1}'.
              format(i + 1, friend.full_name))


def get_friend(friends):
    item_friend = {str(i + 1): friend for i, friend in enumerate(friends)}
    item = get_valid_input(
        "What friend's info do you want to display? ",
        tuple(item_friend.keys())
    )
    return item_friend[item]


def new_line(f):
    def wrapper(*args, **kwargs):
        print()
        f(*args, **kwargs)
        print()
    return wrapper