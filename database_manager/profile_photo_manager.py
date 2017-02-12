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
