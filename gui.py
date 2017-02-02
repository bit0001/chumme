import os

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
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
    return [(friend.full_name,)
            for friend in get_friend_manager().get_friends()]


class ChumMeRoot(BoxLayout):
    add_friend_form = ObjectProperty()
    friend_list_view = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_friend_list_view()

    def update_friend_list_view(self):
        friends = get_friends()
        no_friends_label = self.friend_list_view.no_friends_label
        friend_list = self.friend_list_view.friend_list

        if friends:
            self.hide_label(no_friends_label)
            self.show_list_view(friend_list, friends)
        else:
            self.show_label(no_friends_label, 'There are no friends to show.')
            self.hide_widget(friend_list)

    def show_label(self, no_friends_label, text):
        self.show_widget(no_friends_label)
        no_friends_label.text = text

    def show_list_view(self, list_view, data):
        self.show_widget(list_view)
        list_view.adapter.data.clear()
        list_view.adapter.data.extend(data)
        list_view._trigger_reset_populate()

    def show_widget(self, friend_list):
        friend_list.size_hint_y = 1

    def hide_widget(self, friend_list):
        friend_list.size_hint_y = None
        friend_list.height = '0dp'

    def hide_label(self, no_friends_label):
        self.hide_widget(no_friends_label)
        no_friends_label.text = ''

    def show_add_friend_form(self):
        self.clear_widgets()
        self.add_friend_form = AddFriendForm()
        self.add_widget(self.add_friend_form)

    def show_friend_list(self):
        self.clear_widgets()
        self.update_friend_list_view()
        self.add_widget(self.friend_list_view)

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
    no_friends_label = ObjectProperty()

    def args_converter(self, index, data_item):
        return {'full_name': (data_item[0])}


class FriendItemButton(ListItemButton):
    full_name = StringProperty()


class ChumMeApp(App):
    pass


def main():
    ChumMeApp().run()


if __name__ == '__main__':
    main()
