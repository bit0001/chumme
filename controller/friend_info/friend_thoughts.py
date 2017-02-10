from kivy.uix.label import Label

from database_manager.thought_manager import EmptyThoughtException
from utils.getter import get_thought_manager
from utils.widget import hide_label, show_label, hide_widget, show_widget
from .friend_carousel import FriendInfo


class FriendThoughts(FriendInfo):
    def update_friend_info(self, friend):
        super().update_friend_info(friend)
        thoughts = get_thought_manager().get_thoughts_by_friend_id(
            self.friend.id
        )
        no_thoughts_label = self.no_thoughts_label
        thought_scroll = self.thought_scroll_view

        if thoughts:
            hide_label(no_thoughts_label)
            show_widget(thought_scroll)
            self.display_thoughts(thoughts)
        else:
            show_label(no_thoughts_label,
                       'There are no thoughts about your friend.')
            hide_widget(thought_scroll)

    def display_thoughts(self, thoughts):
        container = self.thought_scroll_view.thought_container
        for thought in thoughts:
            label = ThoughtLabel(text = thought.text)
            container.add_widget(label)

    def add_thought(self, text):
        try:
            get_thought_manager().add_thought(
                self.friend.id, text.strip()
            )
        except EmptyThoughtException:
            # show pop up saying that no empty thought
            pass
        else:
            self.thought_input.text = ''
            self.thought_input.focus = True

class ThoughtLabel(Label):
    pass
