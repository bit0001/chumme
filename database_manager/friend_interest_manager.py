from .db_context_manager import DBContextManager


QUERIES = {
    'create_friends_interests_table':
    """
    CREATE TABLE IF NOT EXISTS friends_interests
    (
      friend_id INTEGER NOT NULL,
      interest_id INTEGER NOT NULL,
      FOREIGN KEY (friend_id) REFERENCES friends(id),
      FOREIGN KEY (interest_id) REFERENCES interests(id),
      PRIMARY KEY (friend_id, interest_id)
    )
    """,
    'insert_friend_interst_id':
    """
    INSERT INTO friends_interests
    VALUES
    (?, ?)
    """,
}

class FriendInterestManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

        with DBContextManager(db_path) as cursor:
            cursor.execute(QUERIES['create_friends_interests_table'])

    def add_friend_interest_ids(self, friend_id: int, interest_id: int):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['insert_friend_interst_id'],
                           (friend_id, interest_id))
