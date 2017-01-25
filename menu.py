import sys

from friend import Friend
from friend_interest_manager import FriendInterestManager
from friend_manager import FriendManager
from interest_manager import InterestManager
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
        db_path = '{}/{}'.format(
            get_absolute_path_of_file_parent_directory(__file__),
            'chumme.db'
        )

        self.friend_manger = FriendManager(db_path)
        self.interest_manager = InterestManager(db_path)
        self.friend_interest_manager = FriendInterestManager(db_path)
        self.choices = {
            '1': self.add_friend,
            '2': self.display_friend_info,
            '3': self.modify_friend_info,
            '4': self.add_friend_interests,
            '5': self.delete_friend,
            '6': self.show_friends,
            '7': self.quit,
        }

    @staticmethod
    def _display_welcome_message():
        print('Welcome to ChumMe!')
        print('This application allows you to keep track of your friends.')

    @staticmethod
    def _display_menu():
        print("""Menu:
1. Add a friend
2. Display friend's info
3. Modify friend's info
4. Add friend's interests
5. Delete friend
6. Show friends
7. Quit
""")


    def run(self):
        self._display_welcome_message()
        while True:
            self._display_menu()
            choice = input('Enter an option: ')

            try:
                self.choices[choice]()
            except KeyError:
                print('"{}" is not a valid choice.'.format(choice))

    @new_line
    def add_friend(self):
        user_input = {
            'first_name': input("Enter your friend's first name: "),
            'last_name': input("Enter your friend's last name: "),
        }
        friend = Friend(**user_input)
        self.friend_manger.add_friend(friend)
        print('Your friend {} has been added.'.format(friend.full_name))

    @new_line
    def display_friend_info(self):
        friends = self.friend_manger.get_friends()
        print_friends(friends, 'display')

        if friends:
            friend = self._get_friend(friends)
            print(friend)

    def _get_friend(self, friends: [Friend]) -> Friend:
        item_friend = {str(i + 1): friend for i, friend in enumerate(friends)}
        item = get_valid_input(
            "What friend's info do you want to display? ",
            tuple(item_friend.keys())
        )
        return item_friend[item]

    @new_line
    def modify_friend_info(self):
        friends = self.friend_manger.get_friends()
        print_friends(friends, 'modify')

        if not friends:
            return

        item_id = self.get_position_friend_id_dict(friends)

        item = get_valid_input(
            'What friend do you want to modify? ', tuple(item_id.keys()))

        for field in Friend.attributes:
            answer = get_valid_input(
                'Do you want to modify {}? (y/n) '.format(field), ('y', 'n'))

            if answer == 'y':
                value = input('Enter value for {}: '.format(field))
                db_field = '_'.join(field.split())
                self.friend_manger.update_friend(item_id[item],db_field, value)
                print('{} has been updated'.format(field.capitalize()))

    def add_friend_interests(self):
        friends = self.friend_manger.get_friends()
        print_friends(friends, 'add interests')

        if not friends:
            return

        item_id = self.get_position_friend_id_dict(friends)

        item = get_valid_input(
            'What friend you do want to add interests? ',
            tuple(item_id.keys())
        )

        interest = input('What interest do you want to add? ')

        interest_id = self.interest_manager.add_interest(interest)

        self.friend_interest_manager.add_friend_interest_ids(
            item_id[item], interest_id
        )

        print('Interest "{}" has been added successfully to {} {}'
              '.'.format(interest,
                         friends[int(item) - 1].first_name,
                         friends[int(item) - 1].last_name))

    def get_position_friend_id_dict(self, friends):
        return {str(i + 1): friend.id for i, friend in enumerate(friends)}

    @new_line
    def delete_friend(self):
        friends = self.friend_manger.get_friends()
        print_friends(friends, 'delete')

        if friends:
            item_id = self.get_position_friend_id_dict(friends)

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
