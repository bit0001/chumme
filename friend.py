class Friend:
    def __init__(self, id: int = 0, first_name: str = '', last_name: str = ''):
        self.id = id
        self.name = first_name
        self.last_name = last_name

    def __repr__(self):
        return 'Name: {0}\nLast Name: {1}'.format(self.name, self.last_name)
