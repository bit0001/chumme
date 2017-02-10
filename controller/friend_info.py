from sqlite3 import IntegrityError

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView

from controller.popup import get_delete_friend_confirmation_popup, \
    get_interest_in_other_interests_popup, get_interest_already_in_list_popup
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
        interest_scroll = self.interest_scroll_view

        if interests:
            hide_label(no_interests_label)
            show_widget(interest_scroll)
            self.display_interests(interests)
        else:
            hide_widget(interest_scroll)
            show_label(no_interests_label, 'There are no interests to show')

    def display_interests(self, interests):
        interest_container = self.interest_scroll_view.interest_container
        interest_container.clear_widgets()
        for interest in interests:
            interest_label = InterestLabel(text=interest)
            interest_container.add_widget(interest_label)


class EditFriendInterests(ModalView):
    friend = ObjectProperty()

    def __init__(self, friend, **kwargs):
        self.friend = friend
        super().__init__(**kwargs)

        self.interests_to_add = set()
        self.interests_to_remove = set()

        friend_interests = get_friend_manager().\
            get_interest_by_friend_id(self.friend.id)
        other_interests = get_interest_manager().get_interests()
        other_interests = set(other_interests) - set(friend_interests)

        for interest in friend_interests:
            interest_button = InterestButton(
                text=interest,
                on_press=self._remove_interest
            )
            self.friend_interests.interest_container.add_widget(interest_button)

        for interest in other_interests:
            interest_button  = InterestButton(
                text=interest,
                on_press=self._add_interest
            )
            self.db_interests.interest_container.add_widget(interest_button)

    def _add_interest(self, instance):
        new_button = InterestButton(
            text=instance.text,
            on_press=self._remove_interest
        )

        self.interests_to_add.add(instance.text)
        self.db_interests.interest_container.remove_widget(instance)
        self.friend_interests.interest_container.add_widget(new_button)

    def add_interest(self, interest):
        if interest in (self.interests_to_add - self.interests_to_remove) or\
            interest in get_friend_manager().\
            get_interest_by_friend_id(self.friend.id):
            self.popup = get_interest_already_in_list_popup(
                interest, self._on_answer)
            self.popup.open()
            return

        try:
            get_interest_manager().add_interest(interest)
        except IntegrityError:
            self.popup = get_interest_in_other_interests_popup(
                interest, self._on_answer)
            self.popup.open()
        else:
            new_button = InterestButton(
                text=interest,
                on_press=self._remove_interest
            )

            self.interests_to_add.add(interest)
            self.friend_interests.interest_container.add_widget(new_button)
            self.interest_text.text = ''

    def _remove_interest(self, instance):
        new_button = InterestButton(
            text=instance.text,
            on_press=self._add_interest
        )

        self.interests_to_remove.add(instance.text)
        self.friend_interests.interest_container.remove_widget(instance)
        self.db_interests.interest_container.add_widget(new_button)

    def update_friend_property(self):
        self.friend = get_friend_manager().\
            get_interest_by_friend_id(self.friend.id)

    def cancel_edition(self):
        self.dismiss()

    def update_interests(self):
        to_add = self.interests_to_add - self.interests_to_remove
        to_remove = self.interests_to_remove - self.interests_to_add

        self.add_interests(to_add)
        self.remove_interests(to_remove)
        self.dismiss()

    def add_interests(self, interests):
        for interest in interests:
            interest_id = get_interest_manager().get_interest_id(interest)
            get_friend_interest_manager().\
                add_friend_interest_ids(self.friend.id, interest_id)

    def remove_interests(self, interests):
        for interest in interests:
            interest_id = get_interest_manager().get_interest_id(interest)
            get_friend_interest_manager().\
                delete_friend_interest_ids(self.friend.id, interest_id)

    def _on_answer(self, instance):
        self.popup.dismiss()
        self.interest_text.text = ''
        self.interest_text.focus = True


class InterestScrollableContainer(ScrollView):
    pass


class InterestLabel(Label):
    pass


class InterestButton(Button):
    pass
