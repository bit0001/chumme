from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.uix.popup import Popup

from database_manager.friend_manager import MinimumFriendParameterException
from friend_info import FriendInfoView
from model.friend import Friend
from popup import OkPopup
from utils.getter import get_friend_manager
from utils.widget import hide_label, show_list_view, show_label, hide_widget


class ChumMeRoot(BoxLayout):
    add_friend_form = ObjectProperty()
    update_friend_form = ObjectProperty()
    friend_list_view = ObjectProperty()
    friend_info_view = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_friend_list_view()

    def update_friend_list_view(self):
        friends = get_friend_manager().get_friends()
        no_friends_label = self.friend_list_view.no_friends_label
        friend_list = self.friend_list_view.friend_list

        if friends:
            hide_label(no_friends_label)
            show_list_view(friend_list, friends)
        else:
            hide_widget(friend_list)
            show_label(no_friends_label, 'There are no friends to show.')

    def show_add_friend_form(self):
        self.clear_widgets()
        self.add_friend_form = AddFriendForm(friend=Friend())
        self.add_widget(self.add_friend_form)

    def show_friend_list(self):
        self.clear_widgets()
        self.update_friend_list_view()
        self.add_widget(self.friend_list_view)

    def add_friend(self):
        friend_form = self.add_friend_form
        parameters = {
            'first_name': friend_form.first_name.text,
            'middle_name': friend_form.middle_name.text,
            'last_name': friend_form.last_name.text,
            'birthdate': friend_form.birthdate.text,
            'email': friend_form.email.text,
            'cell_phone': friend_form.cell_phone.text
        }

        try:
            get_friend_manager().add_friend(Friend(**parameters))
        except AddFriendError:
            content = OkPopup(
                text='First name and last name are mandatory fields.'
            )
            content.bind(on_answer=self._on_answer)

            self.popup = Popup(
                title='Error adding friend',
                content=content,
                auto_dismiss=False)
            self.popup.open()
        else:
            self.show_friend_list()

    def update_friend(self, id):
        pass


    def _on_answer(self, instance):
        self.popup.dismiss()

    def show_friend_details(self, friend):
        self.clear_widgets()
        self.friend_info_view = FriendInfoView()
        self.friend_info_view.update_friend_information(friend)
        self.add_widget(self.friend_info_view)


class FriendForm(BoxLayout):
    pass


class AddFriendForm(FriendForm):
    pass


class FriendList(BoxLayout):
    def args_converter(self, index, data_item):
        return {'friend': data_item}


class FriendItemButton(ListItemButton):
    friend = ObjectProperty()


class ChumMeApp(App):
    pass


def main():
    ChumMeApp().run()


if __name__ == '__main__':
    main()
