from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout


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
