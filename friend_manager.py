from db_context_manager import DBContextManager
from friend import Friend


QUERIES = {
    'create_friends_table':
        """
        CREATE TABLE IF NOT EXISTS friends
        (
          name VARCHAR(50) NOT NULL,
          last_name VARCHAR(50) NOT NULL)
        """,
    'insert_friend':
        """
        INSERT INTO friends VALUES (?, ?)
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
                friends.append(Friend(row[0], row[1]))

        return friends