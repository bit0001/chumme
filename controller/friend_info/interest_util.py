from sqlite3 import IntegrityError

from kivy.uix.button import Button
from kivy.uix.label import Label

from utils.getter import get_interest_manager


class InterestLabel(Label):
    pass


class InterestButton(Button):
    pass


def perform_operation_with_interests(operation, interests, friend):
    for interest in interests:
        interest_id = get_interest_manager().get_interest_id(interest)
        try:
            operation(friend.id, interest_id)
        except IntegrityError:
            pass
