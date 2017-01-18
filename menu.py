import sys

from db_context_manager import DBContextManager
from friend import Friend


class FriendManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

        with DBContextManager(db_path) as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS friends
            (
              name VARCHAR(50) NOT NULL,
              last_name VARCHAR(50) NOT NULL
            )
            """)


class Menu:
    def __init__(self):
        self.friends = []
        self.choices = {
            '1': self.add_friend,
            '2': self.show_friends,
            '3': self.quit,
        }

    @staticmethod
    def _display_welcome_message():
        print('Welcome to ChumMe!')
        print('This application allows you to keep track of your friends.')

    @staticmethod
    def _display_menu():
        print("""Menu:
1. Add a friend
2. Show friends
3. Quit
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

    def add_friend(self):
        name = input("Enter friend's name: ")
        last_name = input("Enter friend's last name: ")
        self.friends.append(Friend(name, last_name))
        print('Your friend {0} {1} has been added.'.format(name, last_name))
        print()

    def show_friends(self):
        if not self.friends:
            print('There are no friends to show.')
            print()
            return

        print('Friends:')
        for friend in self.friends:
            print(friend)
            print()

    def quit(self):
        print('Thank you for using your ChumMe.')
        sys.exit(0)
