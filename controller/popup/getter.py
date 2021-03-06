from kivy.uix.popup import Popup

from controller.popup.popups import OkPopup, ConfirmPopup


def get_ok_popup(title, text, on_answer):
    content = OkPopup(text=text)
    content.bind(on_answer=on_answer)
    return Popup(
        title=title,
        content=content,
        auto_dismiss=False
    )


def get_interest_in_other_interests_popup(interest, on_answer):
    return get_ok_popup(
        title='Interest in Other Interests',
        text="The interest '{}' is in Other Interest. "
             "Please, choose it there.".format(interest),
        on_answer=on_answer
    )


def get_interest_already_in_list_popup(interest, on_answer):
    return get_ok_popup(
        title='Interest in list',
        text="The interest '{}' has been already added.".format(interest),
        on_answer=on_answer
    )

def get_interest_should_not_be_empty_string_popup(on_answer):
    return get_ok_popup(
        title='Interest should not be an empty string',
        text='Please, enter an interest that is not an empty string.',
        on_answer=on_answer
    )


def get_empty_thought_popup(on_answer):
    return get_ok_popup(
        title='Empty thought',
        text='Thought about your friend should not be an empty string or '
             'a string just made of whitespaces.',
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
