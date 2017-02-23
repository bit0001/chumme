from sqlite3 import IntegrityError

from controller.util import get_image_from_blob
from database_manager.friend_manager import MinimumFriendParameterException
from database_manager.util import ChumMeDBManager
from .friend_form import FriendForm


class AddFriendForm(FriendForm):
    def add_friend(self):
        friend = self.build_friend(self.parent.add_friend_form)
        try:
            friend_id = ChumMeDBManager().friend_manager.add_friend(friend)
            self._add_social_networks(friend_id)
            self._add_friend_profile_photo(friend_id)
        except MinimumFriendParameterException:
            self.display_error_popup('adding')
        else:
            self.parent.show_friend_list()

    def _add_social_networks(self, friend_id):
        for i, field in enumerate(self.social_network_fields):
            if field.check_box.active:
                ChumMeDBManager().friend_social_network_manager.\
                    add_friend_social_network(
                    friend_id,
                    i + 1,
                    field.text_input.text
                )

    def _add_friend_profile_photo(self, friend_id):
        if self.blob_profile_image:
            ChumMeDBManager().profile_photo_manager.insert_profile_photo(
                friend_id,
                self.blob_profile_image['blob'],
                self.blob_profile_image['ext']
            )

class UpdateFriendForm(FriendForm):
    def __init__(self, friend, **kwargs):
        super().__init__(friend, **kwargs)
        social_networks = ChumMeDBManager().friend_manager.\
            get_social_network_links_by_friend_id(self.friend.id)

        for i, link in social_networks.items():
            field = self.social_network_fields[i - 1]
            field.text_input.text = link

        profile_image = ChumMeDBManager().profile_photo_manager.\
            select_profile_photo(self.friend.id)

        if profile_image:
            blob = profile_image['blob']
            extension = profile_image['ext'][1:]
            self.image.texture = get_image_from_blob(blob, extension).texture

    def update_friend(self):
        updated_friend = self.build_friend(self.parent.update_friend_form)
        try:
            ChumMeDBManager().friend_manager.update_friend(updated_friend)
            self._update_social_networks()
            self._update_image()
        except MinimumFriendParameterException:
            self.display_error_popup('updating')
        else:
            self.parent.show_friend_details(updated_friend)

    def _update_social_networks(self):
        for i, field in enumerate(self.social_network_fields):
            if field.check_box.active:
                try:
                    ChumMeDBManager().friend_social_network_manager.\
                        add_friend_social_network(
                        self.friend.id,
                        i + 1,
                        field.text_input.text
                    )
                except IntegrityError:
                    ChumMeDBManager().friend_social_network_manager.\
                        update_social_network(
                        field.text_input.text,
                        self.friend.id,
                        i + 1
                    )

    def _update_image(self):
        if self.blob_profile_image:
            try:
                ChumMeDBManager().profile_photo_manager.insert_profile_photo(
                    self.friend.id,
                    self.blob_profile_image['blob'],
                    self.blob_profile_image['ext']
                )
            except IntegrityError:
                ChumMeDBManager().profile_photo_manager.update_profile_photo(
                    self.friend.id,
                    self.blob_profile_image['blob'],
                    self.blob_profile_image['ext']
                )

    def build_friend(self, form):
        friend = super().build_friend(form)
        friend.id = self.friend.id
        return friend
