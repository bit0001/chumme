from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from popup import ConfirmPopup
from utils.getter import get_friend_manager


class FriendInfoView(BoxLayout):
    EMPTY_FIELD = '-'
    friend = ObjectProperty()
    full_name = StringProperty()
    first_name = StringProperty()
    middle_name = StringProperty()
    last_name = StringProperty()
    birthdate = StringProperty()
    email = StringProperty()
    cell_phone = StringProperty()

    def update_friend_information(self, friend):
        self.friend = friend
        self.full_name = friend.full_name
        self.first_name = friend.first_name
        self.middle_name = self.get_field(friend.middle_name)
        self.last_name = friend.last_name
        self.birthdate = self.get_field(friend.birthdate)
        self.email = self.get_field(friend.email)
        self.cell_phone = self.get_field(friend.cell_phone)

    def get_field(self, field):
        return field if field else FriendInfoView.EMPTY_FIELD

    def delete_friend(self):
        content = ConfirmPopup(
            text='Are you sure you want to delete'
                 'your friend {}?'.format(self.friend.full_name))
        content.bind(on_answer=self._on_answer)

        self.popup = Popup(
            title='Deleting friend...',
            content=content,
            auto_dismiss=False
        )

        self.popup.open()

    def _on_answer(self, instance, answer):
        self.popup.dismiss()
        if answer:
            get_friend_manager().delete_friend(self.friend.id)
            self.parent.show_friend_list()
