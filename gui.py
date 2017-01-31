import os

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton

from friend import Friend
from friend_manager import FriendManager


def get_friend_manager():
    db_path = '{}/{}'.format(
        os.path.dirname(os.path.abspath(__file__)),
        'chumme.db'
    )
    return FriendManager(db_path)

def get_friends():
    return [friend.full_name
            for friend in get_friend_manager().get_friends()]


class ChumMeRoot(BoxLayout):
    add_friend_form = ObjectProperty()
    friend_list_view = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        friend_list = self.friend_list_view.friend_list
        friend_list.adapter.data.clear()
        friend_list.adapter.data.extend(get_friends())
        friend_list._trigger_reset_populate()

    def show_add_friend_form(self):
        self.clear_widgets()
        self.add_friend_form = AddFriendForm()
        self.add_widget(self.add_friend_form)

    def show_friend_list(self):
        self.clear_widgets()
        self.add_widget(FriendList())

    def add_friend(self):
        friend = Friend(first_name=self.add_friend_form.first_name_input.text,
                        last_name=self.add_friend_form.last_name_input.text)
        get_friend_manager().add_friend(friend)
        self.show_friend_list()


class AddFriendForm(BoxLayout):
    first_name_input = ObjectProperty()
    last_name_input = ObjectProperty()



class FriendList(BoxLayout):
    friend_list = ObjectProperty()


class FriendItemButton(ListItemButton):
    pass


class ChumMeApp(App):
    pass


def main():
    ChumMeApp().run()


if __name__ == '__main__':
    main()
