class Friend:

    attributes = ['first name', 'middle name', 'last name',
                  'birthdate', 'email', 'cell phone']

    def __init__(self,
                 id: int = 0,
                 first_name: str = '',
                 middle_name: str = None,
                 last_name: str = '',
                 birthdate: str = None,
                 email: str = None,
                 cell_phone: str = None):
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.email = email
        self.cell_phone = cell_phone

    def __repr__(self):
        return 'Name: {0}\nLast Name: {1}'.format(self.first_name, self.last_name)
