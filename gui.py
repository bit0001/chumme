from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from friend_manager import FriendManager
from util import get_absolute_path_of_parent_directory


def get_friend_manager():
    db_path = '{}/{}'.format(
        get_absolute_path_of_parent_directory(__file__),
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
