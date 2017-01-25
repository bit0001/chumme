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

    @property
    def full_name(self):
        if self.middle_name is None:
            return '{} {}'.format(self.first_name, self.last_name)

        return '{} {} {}'.format(
            self.first_name,
            self.middle_name,
            self.last_name)

    def __repr__(self):
        return """First name: {0}
Middle name: {1}
Last Name: {2}
Birthdate: {3}
Email: {4}
Cell phone: {5}
            """.format(self.first_name,
                       self.middle_name,
                       self.last_name,
                       self.birthdate,
                       self.email,
                       self.cell_phone)
