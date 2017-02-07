from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from controller.add_update_form import AddFriendForm, UpdateFriendForm
from controller.friend_info import FriendInfoCarousel
from model.friend import Friend


class ChumMeRoot(BoxLayout):
    add_friend_form = ObjectProperty()
    update_friend_form = ObjectProperty()
    friend_list_view = ObjectProperty()
    friend_info_carousel = ObjectProperty()

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
        self.friend_info_carousel = FriendInfoCarousel()
        self.friend_info_carousel.general_info.update_friend_information(friend)
        self.add_widget(self.friend_info_carousel)
