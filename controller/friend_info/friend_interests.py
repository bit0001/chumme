from sqlite3 import IntegrityError

from kivy.properties import ObjectProperty
from kivy.uix.modalview import ModalView

from controller.popup import get_interest_already_in_list_popup, \
    get_interest_in_other_interests_popup, \
    get_interest_should_not_be_empty_string_popup
from utils.getter import get_friend_manager, get_interest_manager, \
    get_friend_interest_manager
from utils.widget import hide_label, show_widget, hide_widget, show_label
from .friend_carousel import FriendInfo
from .interest_util import perform_operation_with_interests, \
    add_interest_button_to_container, add_interests_to_container, \
    add_interests_to_friend_interests


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
            add_interests_to_friend_interests(
                self.interest_scroll_view.interest_container, interests)
        else:
            hide_widget(interest_scroll)
            show_label(no_interests_label, 'There are no interests to show')


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

        add_interests_to_container(
            self.friend_interests.interest_container,
            friend_interests, self._remove_interest
        )

        add_interests_to_container(
            self.db_interests.interest_container,
            other_interests, self._add_interest
        )

    def _add_interest(self, instance):
        interest = instance.text
        add_interest_button_to_container(
            self.friend_interests.interest_container,
            interest, self._remove_interest
        )

        self.interests_to_add.add(interest)
        self.interests_to_remove.discard(instance.text)
        self.db_interests.interest_container.remove_widget(instance)

    def _remove_interest(self, instance):
        interest = instance.text
        add_interest_button_to_container(
            self.db_interests.interest_container,
            interest, self._add_interest
        )

        self.interests_to_remove.add(interest)
        self.interests_to_add.discard(interest)
        self.friend_interests.interest_container.remove_widget(instance)

    def add_interest(self, interest):
        if not interest:
            self.popup = get_interest_should_not_be_empty_string_popup(
                self._on_answer
            )
            self.popup.open()
            return

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
            add_interest_button_to_container(
                self.friend_interests.interest_container,
                interest, self._remove_interest
            )

            self.interests_to_add.add(interest)
            self.interest_text.text = ''
            self.interest_text.focus = True

    def update_friend_property(self):
        self.friend = get_friend_manager().\
            get_interest_by_friend_id(self.friend.id)

    def cancel_edition(self):
        self.dismiss()

    def update_interests(self):
        self.add_interests(self.interests_to_add)
        self.remove_interests(self.interests_to_remove)
        self.dismiss()

    def add_interests(self, interests):
        perform_operation_with_interests(
            get_friend_interest_manager().add_friend_interest_ids,
            interests, self.friend
        )

    def remove_interests(self, interests):
        perform_operation_with_interests(
            get_friend_interest_manager().delete_friend_interest_ids,
            interests, self.friend
        )

    def _on_answer(self, instance):
        self.popup.dismiss()
        self.interest_text.text = ''
        self.interest_text.focus = True
