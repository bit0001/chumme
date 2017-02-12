import os
from sqlite3 import IntegrityError

from model.social_network import SocialNetwork
from .db_context_manager import DBContextManager

DB_PATH = '{}/{}'.format(
    os.path.dirname(os.path.abspath(__file__)), '../chumme.db'
)

CREATE_TABLES_QUERIES = {
    'create_friends_interests_table':
        """
        CREATE TABLE IF NOT EXISTS friends_interests
        (
          friend_id INTEGER NOT NULL,
          interest_id INTEGER NOT NULL,
          FOREIGN KEY (friend_id)
            REFERENCES friends(id)
            ON DELETE CASCADE,
          FOREIGN KEY (interest_id) REFERENCES interests(id),
          PRIMARY KEY (friend_id, interest_id)
        )
        """,
    'create_friends_table':
        """
        CREATE TABLE IF NOT EXISTS friends
        (
          id INTEGER PRIMARY KEY,
          first_name VARCHAR(50) NOT NULL,
          middle_name VARCHAR(50),
          last_name VARCHAR(50) NOT NULL,
          birthdate DATE,
          email VARCHAR(320),
          cell_phone VARCHAR(50),
          status VARCHAR(30) NOT NULL
        )
        """,
    'create_friends_social_networks_table':
        """
        CREATE TABLE IF NOT EXISTS friends_social_networks
        (
          friend_id INTEGER NOT NULL,
          social_network_id INTEGER NOT NULL,
          social_network_link TEXT NOT NULL,
          FOREIGN KEY (friend_id)
            REFERENCES friends(id)
            ON DELETE CASCADE,
          FOREIGN KEY (social_network_id)
            REFERENCES social_networks(id),
          PRIMARY KEY (friend_id, social_network_id)
        );
        """,
    'create_interests_table':
        """
        CREATE TABLE IF NOT EXISTS interests
        (
          id INTEGER PRIMARY KEY,
          interest VARCHAR(50) NOT NULL UNIQUE
        )
        """,
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
    'create_profile_photos_table':
        """
        CREATE TABLE IF NOT EXISTS profile_photos
        (
          friend_id INTEGER PRIMARY KEY,
          profile_photo BLOB,
          extension VARCHAR(10),
          FOREIGN KEY (friend_id)
            REFERENCES friends(id)
            ON DELETE CASCADE
        )
        """
}

OTHER_QUERIES = {
    'insert_social_network':
        """
        INSERT INTO social_networks
        (social_network_name, base_url, logo_path)
        VALUES
        (?, ?, ?)
        """
}

def create_tables_if_not_exist():
    for query in CREATE_TABLES_QUERIES.values():
        with DBContextManager(DB_PATH) as cursor:
            cursor.execute(query)

    fill_social_networks_table()


def fill_social_networks_table():
    with DBContextManager(DB_PATH) as cursor:
        for social_network in SocialNetwork:
            try:
                cursor.execute(
                    OTHER_QUERIES['insert_social_network'],
                    (social_network.social_network_name,
                     social_network.base_url,
                     social_network.logo_path)
                )
            except IntegrityError:
                pass
