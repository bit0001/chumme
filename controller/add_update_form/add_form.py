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
