class Friend:
    STATUSES = [
        'single', 'in a relationship', 'engaged', 'in civil union', 'married',
        'separated', 'divorced', 'widowed', 'in an open relationship',
        "it's complicated", 'unknown'
    ]

    def __init__(self,
                 id: int = 0,
                 first_name: str = '',
                 middle_name: str = '',
                 last_name: str = '',
                 birthdate: str = '',
                 email: str = '',
                 cell_phone: str = '',
                 status: str = STATUSES[-1],
                 profile_photo=None
                 ):
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.email = email
        self.cell_phone = cell_phone
        self.status = status
        self.profile_photo = profile_photo

    @property
    def full_name(self):
        if self.middle_name is None:
            return '{} {}'.format(self.first_name, self.last_name)

        return '{} {} {}'.format(
            self.first_name,
            self.middle_name,
            self.last_name)

    def __repr__(self):
        return """First name: {}
Middle name: {}
Last Name: {}
Birthdate: {}
Email: {}
Cell phone: {}
Status: {}
            """.format(self.first_name,
                       self.middle_name,
                       self.last_name,
                       self.birthdate,
                       self.email,
                       self.cell_phone,
                       self.status)
