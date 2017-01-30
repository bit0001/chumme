import os
import sys

from friend import Friend
from friend_interest_manager import FriendInterestManager
from friend_manager import FriendManager
from interest_manager import InterestManager
from util import new_line, get_friend, print_friends, get_valid_input


class Menu:
    def __init__(self):
        print(__file__)
        db_path = '{}/{}'.format(
            os.path.dirname(os.path.abspath(__file__)),
            'chumme.db'
        )

        print(db_path)

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
            friend = get_friend(friends)
            print(friend)

    @new_line
    def modify_friend_info(self):
        friends = self.friend_manger.get_friends()
        print_friends(friends, 'modify')

        if friends:
            friend = get_friend(friends)

            for field in Friend.attributes:
                answer = get_valid_input(
                    'Do you want to modify {}? (y/n) '.format(field),
                    ('y', 'n'))

                if answer == 'y':
                    value = input('Enter value for {}: '.format(field))
                    db_field = '_'.join(field.split())
                    self.friend_manger.update_friend(friend.id, db_field,
                                                     value)
                    print('{} has been updated'.format(field.capitalize()))

    def add_friend_interests(self):
        friends = self.friend_manger.get_friends()
        print_friends(friends, 'add interests')

        if friends:
            friend = get_friend(friends)
            interest = input('What interest do you want to add? ')
            interest_id = self.interest_manager.add_interest(interest)

            self.friend_interest_manager.add_friend_interest_ids(
                friend.id, interest_id)

            print('Interest "{}" has been added successfully to {}.'
                  .format(interest, friend.full_name))

    @new_line
    def delete_friend(self):
        friends = self.friend_manger.get_friends()
        print_friends(friends, 'delete')

        if friends:
            friend = get_friend(friends)
            answer = get_valid_input(
                'Are you sure you want to delete '
                'your friend {}? (y/n) '.format(friend.full_name),
                ('y', 'n'))

            if answer == 'y':
                self.friend_manger.delete_friend(friend.id)
                print('{} has been deleted.'.format(friend.full_name))

    @new_line
    def show_friends(self):
        print_friends(self.friend_manger.get_friends(), 'show')

    @new_line
    def quit(self):
        print('Thank you for using ChumMe.')
        sys.exit(0)


def main():
    Menu().run()


if __name__ == '__main__':
    main()
