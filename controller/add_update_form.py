from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from controller.popup import get_add_edit_friend_error_popup
from database_manager.friend_manager import MinimumFriendParameterException
from model.friend import Friend
from utils.getter import get_friend_manager


class FriendForm(BoxLayout):
    friend = ObjectProperty()

    def __init__(self, friend, **kwargs):
        self.friend = friend
        super().__init__(**kwargs)

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
            get_friend_manager().add_friend(friend)
        except MinimumFriendParameterException:
            self.display_error_popup('adding')
        else:
            self.parent.show_friend_list()


class UpdateFriendForm(FriendForm):
    def update_friend(self):
        updated_friend = self.build_friend(self.parent.update_friend_form)
        try:
            get_friend_manager().update_friend(updated_friend)
        except MinimumFriendParameterException:
            self.display_error_popup('updating')
        else:
            self.parent.show_friend_details(updated_friend)

    def build_friend(self, form):
        friend = super().build_friend(form)
        friend.id = self.friend.id
        return friend


class SocialNetworkField(Label):
    pass
