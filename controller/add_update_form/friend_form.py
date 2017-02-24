import os
from sqlite3 import Binary

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

from controller.popup.popup import get_add_edit_friend_error_popup
from model.friend import Friend
from model.social_network import SocialNetwork


class FriendForm(BoxLayout):
    friend = ObjectProperty()

    def __init__(self, friend, **kwargs):
        self.friend = friend
        super().__init__(**kwargs)
        self.blob_profile_image = dict()
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

    def blob_image(self, image):
        with open(image, 'rb') as f:
            file_name, extension = os.path.splitext(image)

            self.blob_profile_image.update(
                {
                    'blob': Binary(f.read()),
                    'ext': extension
                }
            )

    def display_error_popup(self, action):
        self.popup = get_add_edit_friend_error_popup(action, self._on_answer)
        self.popup.open()

    def _on_answer(self, instance):
        self.popup.dismiss()


class SocialNetworkField(BoxLayout):
    def __init__(self, hint, image, **kwargs):
        super().__init__(**kwargs)
        self.hint = hint
        self.image = image

    def enable_disable_text_input(self, checkbox):
        self.text_input.disabled = not checkbox.active


class ImageChooser(ModalView):
    pass
