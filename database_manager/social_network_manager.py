from sqlite3 import IntegrityError

from database_manager.db_context_manager import DBContextManager
from model.social_network import SocialNetwork

QUERIES = {
    'create_social_networks_table':
        """
        CREATE TABLE IF NOT EXISTS social_networks
        (
          id INTEGER PRIMARY KEY,
          social_network_name VARCHAR(50) NOT NULL UNIQUE,
          base_url VARCHAR(200) NOT NULL UNIQUE,
          logo_path TEXT
        )
        """,
    'insert_social_network':
        """
        INSERT INTO social_networks
        (social_network_name, base_url, logo_path)
        VALUES
        (?, ?, ?)
        """
}

class SocialNetworkManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

        with DBContextManager(db_path) as cursor:
            cursor.execute(QUERIES['create_social_networks_table'])

            for social_network in SocialNetwork:
                try:
                    cursor.execute(
                        QUERIES['insert_social_network'],
                        (social_network.social_network_name,
                         social_network.base_url,
                         social_network.logo_path)
                    )
                except IntegrityError:
                    pass
