from sqlite3 import OperationalError

from model.friend import Friend
from .db_context_manager import DBContextManager

QUERIES = {
    'insert_friend':
        """
        INSERT INTO friends
        (
          first_name, middle_name, last_name, birthdate,
          email, cell_phone, status
        )
        VALUES
        (
          trim(?), trim(?), trim(?), trim(?), trim(?), trim(?), ?
        )
        """,
    'update_friend_on_field':
        """
        UPDATE friends
        SET {} = ?
        WHERE id = ?
        """,
    'update_friend':
        """
        UPDATE friends
        SET first_name = ?, middle_name = ?, last_name = ?,
            birthdate = ?, email = ?, cell_phone = ?, status = ?
        WHERE id = ?
        """,
    'delete_friend':
        """
        DELETE FROM friends
        WHERE id = ?
        """,
    'get_friends':
        """
        SELECT * FROM friends
        """,
    'select_interests_by_friend_id':
        """
        SELECT i.interest
        FROM friends f
        INNER JOIN friends_interests fi
        ON f.id = fi.friend_id
        INNER JOIN interests i
        ON fi.interest_id = i.id
        WHERE f.id = ?
        """,
    'select_social_networks_by_friend_id':
        """
        SELECT sn.id, fsn.social_network_link, sn.logo_path
        FROM friends f
        INNER JOIN friends_social_networks fsn
        ON f.id = fsn.friend_id
        INNER JOIN social_networks sn
        ON fsn.social_network_id = sn.id
        WHERE f.id = ?
        """
}


class MinimumFriendParameterException(Exception):
    pass


class FriendManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def add_friend(self, friend: Friend):
        self.check_mandatory_fields(friend)
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(
                QUERIES['insert_friend'],
                (friend.first_name, friend.middle_name, friend.last_name,
                 friend.birthdate, friend.email, friend.cell_phone,
                 friend.status)
            )

            return cursor.lastrowid

    def check_mandatory_fields(self, friend):
        if friend.first_name == '' or friend.last_name == '':
            raise MinimumFriendParameterException()

    def get_friends(self) -> [Friend]:
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['get_friends'])

            friends = []
            for row in cursor.fetchall():
                parameters = {
                    'id': row[0],
                    'first_name': row[1],
                    'middle_name': row[2],
                    'last_name': row[3],
                    'birthdate': row[4],
                    'email': row[5],
                    'cell_phone': row[6],
                    'status': row[7]
                }
                friends.append(Friend(**parameters))

        return friends

    def update_friend(self, friend: Friend):
        self.check_mandatory_fields(friend)
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['update_friend'],
                           (friend.first_name, friend.middle_name,
                            friend.last_name, friend.birthdate,
                            friend.email, friend.cell_phone,
                            friend.status, friend.id))

    def update_friend_on_field(self, id: int, field: str, value: str):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['update_friend_on_field'].format(field),
                           (value, id))

    def delete_friend(self, id: int):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(QUERIES['delete_friend'], (id,))

    def get_interest_by_friend_id(self, id) -> list:
        with DBContextManager(self.db_path) as cursor:
            try:
                cursor.execute(QUERIES['select_interests_by_friend_id'], (id,))
            except OperationalError:
                return []
            else:
                return [row[0] for row in cursor.fetchall()]

    def get_social_network_links_by_friend_id(self, id: int):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(
                QUERIES['select_social_networks_by_friend_id'], (id,)
            )

            return {row[0]: row[1] for row in cursor.fetchall()}

    def get_social_networks_for_general_info_by_friend_id(self, id):
        with DBContextManager(self.db_path) as cursor:
            cursor.execute(
                QUERIES['select_social_networks_by_friend_id'], (id,)
            )

            return {row[2]: row[1] for row in cursor.fetchall()}
