import os
from sqlite3 import IntegrityError

from .friend_interest_manager import FriendInterestManager
from .friend_manager import FriendManager
from .friend_social_network_manager import FriendSocialNetworkManager
from .interest_manager import InterestManager
from .profile_photo_manager import ProfilePhotoManager
from .thought_manager import ThoughtManager
from .queries.create_table import CREATE_TABLES_QUERIES, OTHER_QUERIES
from .db_context_manager import DBContextManager
from model.social_network import SocialNetwork

DB_PATH = '{}/{}'.format(
    os.path.dirname(os.path.abspath(__file__)), '../chumme.db'
)


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


class ChumMeDBManager:
    @staticmethod
    def friend_manager():
        return FriendManager(DB_PATH)

    @staticmethod
    def interest_manager():
        return InterestManager(DB_PATH)

    @staticmethod
    def friend_interest_manager():
        return FriendInterestManager(DB_PATH)

    @staticmethod
    def thought_manager():
        return ThoughtManager(DB_PATH)

    @staticmethod
    def friend_social_network_manager():
        return FriendSocialNetworkManager(DB_PATH)

    @staticmethod
    def profile_photo_manager():
        return ProfilePhotoManager(DB_PATH)
