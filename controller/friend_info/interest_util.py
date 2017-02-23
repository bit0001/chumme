from sqlite3 import IntegrityError

from kivy.uix.button import Button
from kivy.uix.label import Label

from database_manager.util import ChumMeDBManager


class InterestLabel(Label):
    pass


class InterestButton(Button):
    pass


def perform_operation_with_interests(operation, interests, friend):
    for interest in interests:
        interest_id = ChumMeDBManager().\
            interest_manager.get_interest_id(interest)
        try:
            operation(friend.id, interest_id)
        except IntegrityError:
            pass


def add_interest_button_to_container(container, interest, on_press):
    new_button = InterestButton(
        text=interest,
        on_press=on_press
    )
    container.add_widget(new_button)


def add_interest_label_to_container(container, interest):
    label = InterestLabel(text=interest)
    container.add_widget(label)


def add_interests_to_friend_interests(container, interests):
    container.clear_widgets()
    for interest in interests:
        add_interest_label_to_container(container, interest)


def add_interests_to_container(container, interests, on_press):
    for interest in interests:
        add_interest_button_to_container(
            container, interest, on_press
        )
