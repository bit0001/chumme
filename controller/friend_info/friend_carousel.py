from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class FriendInfoCarousel(BoxLayout):
    friend = ObjectProperty()
    general_info = ObjectProperty()
    interests = ObjectProperty()
    thoughts = ObjectProperty()

    def __init__(self, friend, **kwargs):
        self.friend = friend
        super().__init__(**kwargs)


class FriendInfo(BoxLayout):
    friend = ObjectProperty()

    def update_friend_info(self, friend):
        self.friend = friend
