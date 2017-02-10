from sqlite3 import IntegrityError, OperationalError

from .db_context_manager import DBContextManager

QUERIES = {
    'create_interests_table':
    """
    CREATE TABLE IF NOT EXISTS interests
    (
      id INTEGER PRIMARY KEY,
      interest VARCHAR(50) NOT NULL UNIQUE
    )
    """,
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
    """
}


class InterestManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

        with DBContextManager(db_path) as cursor:
            cursor.execute(QUERIES['create_interests_table'])

    def get_interests(self):
        with DBContextManager(self.db_path) as cursor:
            try:
                cursor.execute(QUERIES['select_all_interests'])
            except OperationalError:
                return []
            else:
                return [row[0] for row in cursor.fetchall()]

    def add_interest(self, interest: str) -> int:
        try:
            with DBContextManager(self.db_path) as cursor:
                cursor.execute(QUERIES['insert_interest'], (interest,))
        except IntegrityError:
            pass
        finally:
            with DBContextManager(self.db_path) as cursor:
                cursor.execute(QUERIES['select_interest_id'],
                           (interest,))
                return cursor.fetchone()[0]
