from kivy.uix.label import Label

from controller.popup import get_empty_thought_popup
from database_manager.thought_manager import EmptyThoughtException
from database_manager.util import ChumMeDBManager
from model.thought import Thought
from utils.widget import hide_label, show_label, hide_widget, show_widget
from .friend_carousel import FriendInfo


class FriendThoughts(FriendInfo):
    def update_friend_info(self, friend):
        super().update_friend_info(friend)
        self.thoughts = ChumMeDBManager().\
            thought_manager.get_thoughts_by_friend_id(
            self.friend.id
        )
        no_thoughts_label = self.no_thoughts_label
        thought_scroll = self.thought_scroll_view

        if self.thoughts:
            hide_label(no_thoughts_label)
            show_widget(thought_scroll)
            self.display_thoughts(self.thoughts)
        else:
            show_label(no_thoughts_label,
                       'There are no thoughts about your friend.')
            hide_widget(thought_scroll)

    def display_thoughts(self, thoughts):
        container = self.thought_scroll_view.thought_container
        for thought in thoughts:
            label = ThoughtLabel(thought)
            container.add_widget(label)

    def add_thought(self, text):
        try:
            ChumMeDBManager().thought_manager.add_thought(
                self.friend.id, text.strip()
            )
        except EmptyThoughtException:
            self.popup = get_empty_thought_popup(self._on_answer)
            self.popup.open()
        else:
            if not self.thoughts:
                hide_label(self.no_thoughts_label)
                show_widget(self.thought_scroll_view)

            thought = Thought(text)
            label = ThoughtLabel(thought)
            self.thought_scroll_view.thought_container.add_widget(label)
            self.thought_input.text = ''
            self.thought_input.focus = True

    def _on_answer(self, instance):
        self.popup.dismiss()
        self.thought_input.text = ''
        self.thought_input.focus = True


class ThoughtLabel(Label):
    def __init__(self, thought, **kwargs):
        super().__init__(**kwargs)
        self._format_thougth(thought)

    def _format_thougth(self, thought):
        template = "[b][size=22]{}[/size][/b]\n"\
                   "[i]{}[/i]"
        self.text = template.format(thought.creation_date, thought.text)
