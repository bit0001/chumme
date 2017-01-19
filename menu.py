import sys

from friend import Friend
from friend_manager import FriendManager
from util import get_absolute_path_of_file_parent_directory, get_valid_input, \
    print_friends


def new_line(f):
    def wrapper(*args, **kwargs):
        print()
        f(*args, **kwargs)
        print()
    return wrapper


class Menu:
    def __init__(self):
        self.friend_manger = FriendManager(
            get_absolute_path_of_file_parent_directory(__file__) +
            '/chumme.db')
        self.choices = {
            '1': self.add_friend,
            '2': self.modify_friend,
            '3': self.delete_friend,
            '4': self.show_friends,
            '5': self.quit,
        }

    @staticmethod
    def _display_welcome_message():
        print('Welcome to ChumMe!')
        print('This application allows you to keep track of your friends.')

    @staticmethod
    def _display_menu():
        print("""Menu:
1. Add a friend
2. Modify friend
3. Delete friend
4. Show friends
5. Quit
""")


    def run(self):
        self._display_welcome_message()
        while True:
            self._display_menu()
            choice = input('Enter an option: ')

            try:
                self.choices[choice]()
            except KeyError:
                print('{} is not a valid choice.'.format(choice))

    @new_line
    def add_friend(self):
        user_input = {
            'first_name': input("Enter your friend's first name: "),
            'last_name': input("Enter your friend's last name: "),
        }
        friend = Friend(**user_input)
        self.friend_manger.add_friend(friend)
        print('Your friend {0} {1} has been added.'.
              format(friend.first_name, friend.last_name))

    @new_line
    def modify_friend(self):
        friends = self.friend_manger.get_friends()
        print_friends(friends, 'modify')

        if not friends:
            return

        item_id = {str(i + 1): friend.id for i, friend in enumerate(friends)}

        item = get_valid_input(
            'What friend do you want to modify? ', tuple(item_id.keys()))

        for field in ['first name', 'middle name', 'last name', 'birthdate', 'email', 'cell phone']:
            answer = get_valid_input(
                'Do you want to modify {}? (y/n) '.format(field), ('y', 'n'))

            if answer == 'y':
                value = input('Enter value for {}: '.format(field))
                db_field = '_'.join(field.split())
                self.friend_manger.update_friend(item_id[item],db_field, value)
                print('{} has been updated'.format(field.capitalize()))

    @new_line
    def delete_friend(self):
        friends = self.friend_manger.get_friends()
        print_friends(friends, 'delete')

        if not friends:
            return

        item_id = {str(i + 1): friend.id for i, friend in enumerate(friends)}

        item = get_valid_input(
            'What friend do you want to delete? ',
            tuple(item_id.keys())
        )

        answer = get_valid_input(
            'Are you sure you want to delete this friend? (y/n) ',
            ('y', 'n')
        )

        if answer == 'y':
            self.friend_manger.delete_friend(item_id[item])
            print('Your friend has been deleted.')

    @new_line
    def show_friends(self):
        print_friends(self.friend_manger.get_friends(), 'show')

    @new_line
    def quit(self):
        print('Thank you for using ChumMe.')
        sys.exit(0)
