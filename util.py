import os

from database_manager.friend_manager import FriendManager


def get_friend_manager():
    db_path = '{}/{}'.format(
        os.path.dirname(os.path.abspath(__file__)),
        'chumme.db'
    )
    return FriendManager(db_path)
