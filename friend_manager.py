from db_context_manager import DBContextManager
from friend import Friend


QUERIES = {
    'create_friends_table':
        """
        CREATE TABLE IF NOT EXISTS friends
        (
          id INTEGER PRIMARY KEY,
          first_name VARCHAR(50) NOT NULL,
          middle_name VARCHAR(50),
          last_name VARCHAR(50) NOT NULL,
          birthdate DATE,
          email VARCHAR(320),
          cell_phone VARCHAR(50)
          )
        """,
    'insert_friend':
        """
        INSERT INTO friends
        (first_name, middle_name, last_name, birthdate, email, cell_phone)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
    'update_friend_on_field':
        """
        UPDATE friends
        SET {} = ?
        WHERE id = ?
        """,
    'update_friend':
        """
        UPDATE friends
        SET first_name = ?, middle_name = ?, last_name = ?,
            birthdate = ?, email = ?, cell_phone = ?
        WHERE id = ?
        """,
    'delete_friend':
        """
        DELETE FROM friends
        WHERE id = ?
        """,
    'get_friends':
        """
        SELECT * FROM friends
        """,
}


class AddFriendError(Exception):
    pass


class FriendManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

        with DBContextManager(db_path) as cursor:
            cursor.execute(QUERIES['create_friends_table'])

    def add_friend(self, friend: Friend):
        self.check_mandatory_fields(friend)
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(
                QUERIES['insert_friend'],
                (friend.first_name, friend.middle_name, friend.last_name,
                 friend.birthdate, friend.email, friend.cell_phone)
            )

    def check_mandatory_fields(self, friend):
        if friend.first_name == '' or friend.last_name == '':
            raise AddFriendError()

    def get_friends(self) -> [Friend]:
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['get_friends'])

            friends = []
            for row in cursor.fetchall():
                parameters = {
                    'id': row[0],
                    'first_name': row[1],
                    'middle_name': row[2],
                    'last_name': row[3],
                    'birthdate': row[4],
                    'email': row[5],
                    'cell_phone': row[6],
                }
                friends.append(Friend(**parameters))

        return friends

    def update_friend(self, friend: Friend):
        self.check_mandatory_fields(friend)
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['update_friend'],
                           (friend.first_name, friend.middle_name,
                            friend.last_name, friend.birthdate,
                            friend.email, friend.cell_phone,
                            friend.id))

    def update_friend_on_field(self, id: int, field: str, value: str):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['update_friend_on_field'].format(field),
                           (value, id))

    def delete_friend(self, id: int):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['delete_friend'], (id,))
