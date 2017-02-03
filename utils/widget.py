def show_widget(friend_list):
    friend_list.size_hint_y = 1


def show_label(no_friends_label, text):
    show_widget(no_friends_label)
    no_friends_label.text = text


def show_list_view(list_view, data):
    show_widget(list_view)
    list_view.adapter.data.clear()
    list_view.adapter.data.extend(data)
    list_view._trigger_reset_populate()


def hide_widget(friend_list):
    friend_list.size_hint_y = None
    friend_list.height = '0dp'


def hide_label(no_friends_label):
    hide_widget(no_friends_label)
    no_friends_label.text = ''
