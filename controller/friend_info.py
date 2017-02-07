from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

from controller.popup import get_delete_friend_confirmation_popup
from utils.getter import get_friend_manager


class FriendInfoCarousel(BoxLayout):
    friend = ObjectProperty()
    general_info = ObjectProperty()
    interests = ObjectProperty()

    def __init__(self, friend, **kwargs):
        self.friend = friend
        super().__init__(**kwargs)


class FriendInfo(BoxLayout):
    friend = ObjectProperty()

    def update_friend_info(self, friend):
        self.friend = friend


class FriendGeneralInfo(FriendInfo):
    EMPTY_FIELD = '-'
    first_name = StringProperty()
    middle_name = StringProperty()
    last_name = StringProperty()
    birthdate = StringProperty()
    email = StringProperty()
    cell_phone = StringProperty()
    status = StringProperty()

    def update_friend_info(self, friend):
        super().update_friend_info(friend)
        self.first_name = friend.first_name
        self.middle_name = self.get_field(friend.middle_name)
        self.last_name = friend.last_name
        self.birthdate = self.get_field(friend.birthdate)
        self.email = self.get_field(friend.email)
        self.cell_phone = self.get_field(friend.cell_phone)
        self.status = friend.status

    def get_field(self, field):
        return field if field else self.EMPTY_FIELD

    def delete_friend(self):
        self.popup = get_delete_friend_confirmation_popup(
            self.friend, self._on_answer)
        self.popup.open()

    def _on_answer(self, instance, answer):
        self.popup.dismiss()
        if answer:
            get_friend_manager().delete_friend(self.friend.id)
            self.parent.show_friend_list()


class FriendInterests(FriendInfo):
    pass
