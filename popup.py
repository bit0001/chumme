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
