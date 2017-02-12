from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from controller.popup import get_add_edit_friend_error_popup
from database_manager.friend_manager import MinimumFriendParameterException
from model.friend import Friend
from model.social_network import SocialNetwork
from utils.getter import get_friend_manager, get_friend_social_network_manager


class FriendForm(BoxLayout):
    friend = ObjectProperty()

    def __init__(self, friend, **kwargs):
        self.friend = friend
        super().__init__(**kwargs)
        container = self.social_network_form.container
        self.social_network_fields = []

        for social_network in SocialNetwork:
            social_network_field = SocialNetworkField(
                hint=social_network.social_network_name,
                image=social_network.logo_path
            )
            self.social_network_fields.append(social_network_field)
            container.add_widget(social_network_field)

    def build_friend(self, form):
        parameters = {
            'first_name': form.first_name.text,
            'middle_name': form.middle_name.text,
            'last_name': form.last_name.text,
            'birthdate': form.birthdate.text,
            'email': form.email.text,
            'cell_phone': form.cell_phone.text,
            'status': form.status.text
        }
        friend = Friend(**parameters)

        return friend

    def display_error_popup(self, action):
        self.popup = get_add_edit_friend_error_popup(action, self._on_answer)
        self.popup.open()

    def _on_answer(self, instance):
        self.popup.dismiss()


class AddFriendForm(FriendForm):
    def add_friend(self):
        friend = self.build_friend(self.parent.add_friend_form)
        try:
            friend_id = get_friend_manager().add_friend(friend)
            self._add_social_networks(friend_id)
        except MinimumFriendParameterException:
            self.display_error_popup('adding')
        else:
            self.parent.show_friend_list()

    def _add_social_networks(self, friend_id):
        for i, field in enumerate(self.social_network_fields):
            if field.check_box.active:
                get_friend_social_network_manager().\
                    add_friend_social_network(
                    friend_id,
                    i + 1,
                    field.text_input.text
                )

class UpdateFriendForm(FriendForm):
    def update_friend(self):
        updated_friend = self.build_friend(self.parent.update_friend_form)
        try:
            get_friend_manager().update_friend(updated_friend)
            self._update_social_networks()
        except MinimumFriendParameterException:
            self.display_error_popup('updating')
        else:
            self.parent.show_friend_details(updated_friend)

    def _update_social_networks(self):
        for i, field in enumerate(self.social_network_fields):
            if field.check_box.active:
                get_friend_social_network_manager().\
                    update_social_network(
                    field.text_input.text,
                    self.friend.id,
                    i + 1
                )

    def build_friend(self, form):
        friend = super().build_friend(form)
        friend.id = self.friend.id
        return friend


class SocialNetworkField(BoxLayout):
    def __init__(self, hint, image, **kwargs):
        super().__init__(**kwargs)
        self.hint = hint
        self.image = image

    def enable_disable_text_input(self, checkbox):
        self.text_input.disabled = not checkbox.active
