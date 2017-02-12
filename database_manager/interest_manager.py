from sqlite3 import IntegrityError, OperationalError

from .db_context_manager import DBContextManager

QUERIES = {
    'insert_interest':
    """
    INSERT INTO interests
    (interest)
    VALUES
    (?)
    """,
    'select_interest_id':
    """
    SELECT id FROM interests
    WHERE interest = ?
    """,
    'select_all_interests':
    """
    SELECT interest FROM interests
    ORDER BY interest
    """
}


class InterestManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_interests(self):
        with DBContextManager(self.db_path) as cursor:
            try:
                cursor.execute(QUERIES['select_all_interests'])
            except OperationalError:
                return []
            else:
                return [row[0] for row in cursor.fetchall()]

    def add_interest(self, interest: str):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['insert_interest'], (interest,))

    def get_interest_id(self, interest) -> int:
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['select_interest_id'],
                           (interest,))
            return cursor.fetchone()[0]
