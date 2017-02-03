from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton

from utils.getter import get_friend_manager
from utils.widget import hide_label, hide_widget, show_label
from utils.widget import show_list_view


class FriendList(BoxLayout):
    def args_converter(self, index, data_item):
        return {'friend': data_item}

    def update(self):
        friends = get_friend_manager().get_friends()
        no_friends_label = self.no_friends_label
        friend_list = self.friend_list

        if friends:
            hide_label(no_friends_label)
            show_list_view(friend_list, friends)
        else:
            hide_widget(friend_list)
            show_label(no_friends_label, 'There are no friends to show.')


class FriendItemButton(ListItemButton):
    friend = ObjectProperty()

