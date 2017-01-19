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
        (first_name, last_name)
        VALUES (?, ?)
        """,
    'update_friend':
        """
        UPDATE friends
        SET {} = ?
        WHERE id = ?
        """,
    'get_friends':
        """
        SELECT * FROM friends
        """,
}


class FriendManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

        with DBContextManager(db_path) as cursor:
            cursor.execute(QUERIES['create_friends_table'])

    def add_friend(self, friend: Friend):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(
                QUERIES['insert_friend'],
                (friend.name, friend.last_name))

    def get_friends(self) -> [Friend]:
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['get_friends'])

            friends = []
            for row in cursor.fetchall():
                friends.append(Friend(row[0], row[1], row[3]))

        return friends

    def update_friend(self, id: int, field: str, value: str):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['update_friend'].format(field),
                           (value, id))
