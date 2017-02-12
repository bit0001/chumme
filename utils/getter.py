import os

from database_manager.friend_interest_manager import FriendInterestManager
from database_manager.friend_manager import FriendManager
from database_manager.friend_social_network_manager import \
    FriendSocialNetworkManager
from database_manager.interest_manager import InterestManager
from database_manager.profile_photo_manager import ProfilePhotoManager
from database_manager.thought_manager import ThoughtManager
from database_manager.util import DB_PATH


def get_friend_manager():
    return FriendManager(DB_PATH)


def get_interest_manager():
    return InterestManager(DB_PATH)


def get_friend_interest_manager():
    return FriendInterestManager(DB_PATH)


def get_thought_manager():
    return ThoughtManager(DB_PATH)


def get_friend_social_network_manager():
    return FriendSocialNetworkManager(DB_PATH)


def get_profile_photo_manager():
    return ProfilePhotoManager(DB_PATH)
