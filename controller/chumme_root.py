from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from controller.friend_info.friend_carousel import FriendInfoCarousel
from model.friend import Friend
from .add_update_form.add_update_form import AddFriendForm, \
    UpdateFriendForm, ImageChooser
from .friend_info.edit_friend_interests import EditFriendInterests


class ChumMeRoot(BoxLayout):
    add_friend_form = ObjectProperty()
    update_friend_form = ObjectProperty()
    friend_list_view = ObjectProperty()
    friend_info_carousel = ObjectProperty()
    edit_friend_interests = ObjectProperty()
    image_chooser = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.friend_list_view.update()

    def show_add_friend_form(self):
        self.clear_widgets()
        self.add_friend_form = AddFriendForm(friend=Friend())
        self.add_widget(self.add_friend_form)

    def show_update_friend_form(self, friend):
        self.clear_widgets()
        self.update_friend_form = UpdateFriendForm(friend=friend)
        self.add_widget(self.update_friend_form)

    def show_friend_list(self):
        self.clear_widgets()
        self.friend_list_view.update()
        self.add_widget(self.friend_list_view)

    def show_friend_details(self, friend):
        self.clear_widgets()
        self.friend_info_carousel = FriendInfoCarousel(friend)
        self.friend_info_carousel.general_info.update_friend_info(friend)
        self.show_friend_interests(friend)
        self.friend_info_carousel.thoughts.update_friend_info(friend)
        self.add_widget(self.friend_info_carousel)

    def show_edit_interests_view(self, friend):
        self.edit_friend_interests = EditFriendInterests(friend)
        self.edit_friend_interests.open()

    def show_friend_interests(self, friend):
        self.friend_info_carousel.interests.update_friend_info(friend)

    def show_image_chooser(self):
        self.image_chooser = ImageChooser()
        self.image_chooser.open()

    def show_friend_form(self, image=None):
        child_widget = self.children[0]
        if image:
            child_widget.image.source = image
            child_widget.blob_image(image)
        self.image_chooser.dismiss()
