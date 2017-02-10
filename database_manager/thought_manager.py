from database_manager.db_context_manager import DBContextManager


QUERIES = {
    'create_thoughts_table':
        """
        CREATE TABLE IF NOT EXISTS thoughts
        (
          friend_id INTEGER NOT NULL,
          thought TEXT NOT NULL,
          creation_date DATETIME,
          FOREIGN KEY (friend_id)
            REFERENCES friends(id)
            ON DELETE CASCADE
        )
        """,
    'insert_thought':
        """
        INSERT INTO thoughts
        VALUES
        (?, ?, datetime('now',  'localtime'))
        """,
    'select_thoughts_by_friend_id':
        """
        SELECT thought, creation_date FROM thoughts t
        INNER JOIN friends f
        ON f.id = t.friend_id
        WHERE f.id = ?
        """
}


class EmptyThoughtException(Exception):
    pass


class ThoughtManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

        with DBContextManager(db_path) as cursor:
            cursor.execute(QUERIES['create_thoughts_table'])

    def add_thought(self, friend_id: int, thought: str):
        if thought is '':
            raise EmptyThoughtException

        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['insert_thought'],
                           (friend_id, thought))

    def get_thoughts_by_friend_id(self, friend_id: int) -> list:
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['select_thoughts_by_friend_id'],
                           (friend_id,))

            return [row[0] for row in cursor.fetchall()]
