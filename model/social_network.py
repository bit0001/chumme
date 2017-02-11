import os
from collections import namedtuple
from enum import Enum, unique

SocialNetworkRecord = namedtuple(
    'SocialNetworkRecord',
    'social_network_name base_url logo'.split()
)


@unique
class SocialNetwork(Enum):
    FACEBOOK = SocialNetworkRecord(
        social_network_name='Facebook',
        base_url='https://www.facebook.com/',
        logo='facebook.png'
    )

    def __init__(self, *social_network):
        self.social_network = SocialNetworkRecord(*social_network)


    @property
    def social_network_name(self):
        return self.social_network.social_network_name

    @property
    def base_url(self):
        return self.social_network.base_url

    @property
    def logo_path(self):
        template = '{}/../resources/img/social_networks/{}'
        path_to_file = os.path.dirname(os.path.abspath(__file__))
        return template.format(path_to_file, self.social_network.logo)
