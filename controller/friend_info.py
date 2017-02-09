from sqlite3 import IntegrityError

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView

from controller.popup import get_delete_friend_confirmation_popup, \
    get_repeated_interest_popup
from utils.getter import get_friend_manager, get_interest_manager, \
    get_friend_interest_manager
from utils.widget import hide_label, show_widget, hide_widget, show_label


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
            self.parent.parent.parent.parent.show_friend_list()


class FriendInterests(FriendInfo):
    def update_friend_info(self, friend):
        super().update_friend_info(friend)
        interests = get_friend_manager().get_interest_by_friend_id(
            self.friend.id)
        no_interests_label = self.no_interests_label


        if interests:
            hide_label(no_interests_label)
            show_widget(self.interests_container)
            self.display_interests(interests)
        else:
            hide_widget(self.interests_container)
            show_label(no_interests_label, 'There are no interests to show')

    def display_interests(self, interests):
        for interest in interests:
            interest_label = InterestLabel(text=interest)
            self.interests_container.add_widget(interest_label)


class EditFriendInterests(ModalView):
    friend = ObjectProperty()

    def __init__(self, friend, **kwargs):
        self.friend = friend
        super().__init__(**kwargs)

    def cancel_edition(self):
        self.dismiss()

    def append_interest(self, interest):
        interest_id = get_interest_manager().add_interest(interest)
        try:
            get_friend_interest_manager().add_friend_interest_ids(
                self.friend.id, interest_id
            )
        except IntegrityError:
            self.popup = get_repeated_interest_popup(
                interest, self._on_answer)
            self.popup.open()

    def _on_answer(self, instance):
        self.popup.dismiss()


class InterestLabel(Label):
    pass
