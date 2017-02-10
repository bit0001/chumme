import datetime


class Thought:
    def __init__(self, text, creation_date=None):
        self.text = text

        self.creation_date = creation_date if\
            creation_date else\
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
