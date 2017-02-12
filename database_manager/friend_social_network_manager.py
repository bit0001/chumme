from database_manager.db_context_manager import DBContextManager

QUERIES = {
    'insert_friend_social_network':
        """
        INSERT INTO friends_social_networks
        VALUES
        (?, ?, ?)
        """,
    'update_social_network':
        """
        UPDATE friends_social_networks
        SET social_network_link = ?
        WHERE friend_id = ? AND social_network_id = ?
        """
}


class FriendSocialNetworkManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def add_friend_social_network(
            self, friend_id, social_network_id, social_network_link):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(
                QUERIES['insert_friend_social_network'],
                (friend_id, social_network_id, social_network_link)
            )

    def update_social_network(self, link, friend_id, social_network_id):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(
                QUERIES['update_social_network'],
                (link, friend_id, social_network_id)
            )
