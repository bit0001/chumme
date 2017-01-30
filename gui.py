import os

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from friend_manager import FriendManager


def get_friend_manager():
    db_path = '{}/{}'.format(
        os.path.dirname(os.path.abspath(__file__)),
        'chumme.db'
    )
    return FriendManager(db_path)


class FriendList(BoxLayout):
    friend_list = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.friend_list.item_strings = [
            friend.full_name for friend in get_friend_manager().get_friends()
            ]


class ChumMeApp(App):
    pass


def main():
    ChumMeApp().run()


if __name__ == '__main__':
    ChumMeApp().run()
