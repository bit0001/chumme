from db_context_manager import DBContextManager
from friend import Friend


class FriendManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

        with DBContextManager(db_path) as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS friends
            (
              name VARCHAR(50) NOT NULL,
              last_name VARCHAR(50) NOT NULL
            )
            """)

    def add_friend(self, friend: Friend):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute("""
            INSERT INTO friends VALUES
            (?, ?)
            """, (friend.name, friend.last_name))

    def get_friends(self) -> [Friend]:
        with DBContextManager(self.db_path) as cursor:
            cursor.execute("""
            SELECT * FROM friends
            """)

            friends = []
            for row in cursor.fetchall():
                friends.append(Friend(row[0], row[1]))

        return friends