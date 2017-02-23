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
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


    def __init__(self):
        self._friend_manager = FriendManager(DB_PATH)
        self._interest_manager = InterestManager(DB_PATH)
        self._friend_interest_manager = FriendInterestManager(DB_PATH)
        self._thought_manager = ThoughtManager(DB_PATH)
        self._friend_social_network_manager = \
            FriendSocialNetworkManager(DB_PATH)
        self._profile_photo_manager = ProfilePhotoManager(DB_PATH)

    @property
    def friend_manager(self):
        return self._friend_manager

    @property
    def interest_manager(self):
        return self._interest_manager

    @property
    def friend_interest_manager(self):
        return self._friend_interest_manager

    @property
    def thought_manager(self):
        return self._thought_manager

    @property
    def friend_social_network_manager(self):
        return self._friend_social_network_manager

    @property
    def profile_photo_manager(self):
        return self._profile_photo_manager
