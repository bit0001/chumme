import os

from database_manager.friend_interest_manager import FriendInterestManager
from database_manager.friend_manager import FriendManager
from database_manager.interest_manager import InterestManager

DB_PATH = '{}/{}'.format(
    os.path.dirname(os.path.abspath(__file__)), '../chumme.db'
)


def get_friend_manager():
    return FriendManager(DB_PATH)


def get_interest_manager():
    return InterestManager(DB_PATH)


def get_friend_interest_manager():
    return FriendInterestManager(DB_PATH)
