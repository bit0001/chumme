import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from friend_manager import FriendManager


def get_friend_manager():
    db_path = '{}/{}'.format(
        os.path.dirname(os.path.abspath(__file__)),
        'chumme.db'
    )
    return FriendManager(db_path)


class ChumMeRoot(BoxLayout):
    def show_add_friend_form(self):
        self.clear_widgets()
        self.add_widget(AddFriendForm())


class AddFriendForm(BoxLayout):
    pass



class FriendList(BoxLayout):
    def get_friends(self):
        return [friend.full_name
                for friend in get_friend_manager().get_friends()]


class ChumMeApp(App):
    pass


def main():
    ChumMeApp().run()


if __name__ == '__main__':
    main()
