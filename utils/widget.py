def show_widget(widget):
    widget.size_hint_y = 1
    widget.size_hint_x = 1


def show_label(label, text):
    show_widget(label)
    label.text = text


def show_list_view(list_view, data):
    show_widget(list_view)
    list_view.adapter.data.clear()
    list_view.adapter.data.extend(data)
    list_view._trigger_reset_populate()


def hide_widget(widget):
    widget.size_hint = (None, None)
    widget.height = '0dp'
    widget.width = '0dp'


def hide_label(label):
    hide_widget(label)
    label.text = ''
