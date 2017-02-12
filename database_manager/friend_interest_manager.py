from .db_context_manager import DBContextManager


QUERIES = {
    'insert_friend_interest_ids':
    """
    INSERT INTO friends_interests
    VALUES
    (?, ?)
    """,
    'delete_friend_interest_ids':
    """
    DELETE FROM friends_interests
    WHERE friend_id = ? AND interest_id = ?
    """
}

class FriendInterestManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def add_friend_interest_ids(self, friend_id: int, interest_id: int):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['insert_friend_interest_ids'],
                           (friend_id, interest_id))

    def delete_friend_interest_ids(self, friend_id: int, interest_id: int):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['delete_friend_interest_ids'],
                           (friend_id, interest_id))
