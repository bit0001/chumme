from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


class PopupLayout(BoxLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super().__init__(**kwargs)

    def on_answer(self, *args):
        pass


class ConfirmPopup(PopupLayout):
    pass


class OkPopup(PopupLayout):
    pass


def get_ok_popup(title, text, on_answer):
    content = OkPopup(text=text)
    content.bind(on_answer=on_answer)
    return Popup(
        title=title,
        content=content,
        auto_dismiss=False
    )


def get_repeated_interest_popup(interest, on_answer):
    return get_ok_popup(
        title='Interest in Other Interests',
        text="The interest '{}' is in Other Interest. "
             "Please, choose it there.".format(interest),
        on_answer=on_answer
    )


def get_add_edit_friend_error_popup(action, on_answer):
    return get_ok_popup(
        title='Error {} friend'.format(action),
        text='First name and last name are mandatory fields.',
        on_answer=on_answer
    )


def get_delete_friend_confirmation_popup(friend, on_answer):
    content = ConfirmPopup(
        text='Are you sure you want to delete '
             'your friend {}?'.format(friend.full_name))
    content.bind(on_answer=on_answer)

    return Popup(
        title='Deleting friend...',
        content=content,
        auto_dismiss=False
    )
