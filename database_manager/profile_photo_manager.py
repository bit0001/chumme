from database_manager.db_context_manager import DBContextManager

QUERIES = {
    'select_profile_photo':
        """
        SELECT profile_photo, extension
        FROM profile_photos
        WHERE friend_id = ?
        """,
    'insert_profile_photo':
        """
        INSERT INTO profile_photos
        VALUES
        (?, ?, ?)
        """,
    'update_profile_photo':
        """
        UPDATE profile_photos
        SET profile_photo = ?, extension = ?
        WHERE friend_id = ?
        """
}


class ProfilePhotoManager():
    def __init__(self, db_path):
        self.db_path = db_path

    def select_profile_photo(self, friend_id):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['select_profile_photo'], (friend_id,))

            row = cursor.fetchone()
            if row:
                return {'blob': row[0], 'ext': row[1]}

            return {}

    def insert_profile_photo(self, friend_id, blob_image, extension):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(
                QUERIES['insert_profile_photo'],
                (friend_id, blob_image, extension)
            )

    def update_profile_photo(self, friend_id, blob_image, extension):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(
                QUERIES['update_profile_photo'],
                (blob_image, extension, friend_id)
            )
