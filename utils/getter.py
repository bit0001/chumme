import os

from database_manager.friend_interest_manager import FriendInterestManager
from database_manager.friend_manager import FriendManager
from database_manager.interest_manager import InterestManager
from database_manager.social_network_manager import SocialNetworkManager
from database_manager.thought_manager import ThoughtManager

DB_PATH = '{}/{}'.format(
    os.path.dirname(os.path.abspath(__file__)), '../chumme.db'
)


def get_friend_manager():
    return FriendManager(DB_PATH)


def get_interest_manager():
    return InterestManager(DB_PATH)


def get_friend_interest_manager():
    return FriendInterestManager(DB_PATH)


def get_thought_manager():
    return ThoughtManager(DB_PATH)


def get_social_network_manager():
    return SocialNetworkManager(DB_PATH)
