import webbrowser

from kivy.properties import StringProperty
from kivy.uix.button import Button

from controller.util import get_image_from_blob
from .friend_carousel import FriendInfo
from controller.popup import get_delete_friend_confirmation_popup
from utils.getter import get_friend_manager, get_profile_photo_manager


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

        profile_photo = get_profile_photo_manager().\
            select_profile_photo(friend.id)

        if profile_photo:
            blob = profile_photo['blob']
            extension = profile_photo['ext'][1:]
            self.profile_photo.texture = get_image_from_blob(blob, extension).texture

    def _show_social_networks(self, friend):
        social_networks = get_friend_manager().\
            get_social_networks_for_general_info_by_friend_id(friend.id)
        container = self.social_network_info.social_network_container.container

        for image, link in social_networks.items():
            button = SocialNetworkButton(image, link)
            container.add_widget(button)

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


class SocialNetworkButton(Button):
    def __init__(self, image, link, **kw):
        super().__init__(**kw)
        self.image = image
        self.link = link

    def open_url(self):
        webbrowser.open(self.link, new=2)
