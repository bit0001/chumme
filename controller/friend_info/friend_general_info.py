from kivy.properties import StringProperty

from .friend_carousel import FriendInfo
from controller.popup import get_delete_friend_confirmation_popup
from utils.getter import get_friend_manager


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
        self._show_social_networks(friend)

    def _show_social_networks(self, friend):
        social_networks = get_friend_manager().\
            get_social_network_links_by_friend_id(friend.id)

        print(social_networks)

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
            self.parent.parent.parent.parent.show_friend_list()
