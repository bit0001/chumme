from utils.getter import ChumMeDBManager
from utils.widget import hide_label, show_widget, hide_widget, show_label
from .friend_carousel import FriendInfo
from .interest_util import add_interests_to_friend_interests


class FriendInterests(FriendInfo):
    def update_friend_info(self, friend):
        super().update_friend_info(friend)
        interests = ChumMeDBManager.friend_manager().get_interest_by_friend_id(
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
