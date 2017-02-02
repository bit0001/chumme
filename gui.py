import os

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.uix.popup import Popup

from friend import Friend
from friend_manager import FriendManager, AddFriendError


def get_friend_manager():
    db_path = '{}/{}'.format(
        os.path.dirname(os.path.abspath(__file__)),
        'chumme.db'
    )
    return FriendManager(db_path)


class ChumMeRoot(BoxLayout):
    add_friend_form = ObjectProperty()
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
            self.hide_label(no_friends_label)
            self.show_list_view(friend_list, friends)
        else:
            self.show_label(no_friends_label, 'There are no friends to show.')
            self.hide_widget(friend_list)

    def show_label(self, no_friends_label, text):
        self.show_widget(no_friends_label)
        no_friends_label.text = text

    def show_list_view(self, list_view, data):
        self.show_widget(list_view)
        list_view.adapter.data.clear()
        list_view.adapter.data.extend(data)
        list_view._trigger_reset_populate()

    def show_widget(self, friend_list):
        friend_list.size_hint_y = 1

    def hide_widget(self, friend_list):
        friend_list.size_hint_y = None
        friend_list.height = '0dp'

    def hide_label(self, no_friends_label):
        self.hide_widget(no_friends_label)
        no_friends_label.text = ''

    def show_add_friend_form(self):
        self.clear_widgets()
        self.add_friend_form = AddFriendForm()
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

    def _on_answer(self, instance):
        self.popup.dismiss()

    def show_friend_details(self, friend):
        self.clear_widgets()
        self.friend_info_view = FriendInfoView()
        self.friend_info_view.update_friend_information(friend)
        self.add_widget(self.friend_info_view)


class AddFriendForm(BoxLayout):
    pass


class FriendInfoView(BoxLayout):
    EMPTY_FIELD = '-'
    friend = ObjectProperty()
    full_name = StringProperty()
    first_name = StringProperty()
    middle_name = StringProperty()
    last_name = StringProperty()
    birthdate = StringProperty()
    email = StringProperty()
    cell_phone = StringProperty()

    def update_friend_information(self, friend):
        self.friend = friend
        self.full_name = friend.full_name
        self.first_name = friend.first_name
        self.middle_name = self.get_field(friend.middle_name)
        self.last_name = friend.last_name
        self.birthdate = self.get_field(friend.birthdate)
        self.email = self.get_field(friend.email)
        self.cell_phone = self.get_field(friend.cell_phone)

    def get_field(self, field):
        return field if field else FriendInfoView.EMPTY_FIELD

    def delete_friend(self):
        content = ConfirmPopup(
            text='Are you sure you want to delete'
                 'your friend {}?'.format(self.friend.full_name))
        content.bind(on_answer=self._on_answer)

        self.popup = Popup(
            title='Deleting friend...',
            content=content,
            auto_dismiss=False
        )

        self.popup.open()

    def _on_answer(self, instance, answer):
        self.popup.dismiss()
        if answer:
            get_friend_manager().delete_friend(self.friend.id)
            self.parent.show_friend_list()


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
