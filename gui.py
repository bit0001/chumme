from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from add_update_form import AddFriendForm
from add_update_form import UpdateFriendForm
from friend_info import FriendInfoView
from model.friend import Friend


class ChumMeRoot(BoxLayout):
    add_friend_form = ObjectProperty()
    update_friend_form = ObjectProperty()
    friend_list_view = ObjectProperty()
    friend_info_view = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.friend_list_view.update()

    def show_add_friend_form(self):
        self.clear_widgets()
        self.add_friend_form = AddFriendForm(friend=Friend())
        self.add_widget(self.add_friend_form)

    def show_update_friend_form(self, friend):
        self.clear_widgets()
        self.update_friend_form = UpdateFriendForm(friend=friend)
        self.add_widget(self.update_friend_form)

    def show_friend_list(self):
        self.clear_widgets()
        self.friend_list_view.update()
        self.add_widget(self.friend_list_view)

    def show_friend_details(self, friend):
        self.clear_widgets()
        self.friend_info_view = FriendInfoView()
        self.friend_info_view.update_friend_information(friend)
        self.add_widget(self.friend_info_view)


class ChumMeApp(App):
    pass


def main():
    ChumMeApp().run()


if __name__ == '__main__':
    main()
