import os
from sqlite3 import IntegrityError

from .queries.queries import CREATE_TABLES_QUERIES, OTHER_QUERIES
from model.social_network import SocialNetwork
from .db_context_manager import DBContextManager

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
