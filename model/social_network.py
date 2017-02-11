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
    TWITTER = SocialNetworkRecord(
        social_network_name='Twitter',
        base_url='https://twitter.com/',
        logo='twitter.png'
    )
    LINKEDIN = SocialNetworkRecord(
        social_network_name='LinkedIn',
        base_url='https://www.linkedin.com/',
        logo='linkedin.png'
    )
    GOOGLE_PLUS = SocialNetworkRecord(
        social_network_name='Google+',
        base_url='https://plus.google.com/',
        logo='google_plus.png'
    )
    INSTAGRAM = SocialNetworkRecord(
        social_network_name='Instagram',
        base_url='https://www.instagram.com/',
        logo='instagram.png'
    )
    PINTEREST = SocialNetworkRecord(
        social_network_name='Pinterest',
        base_url='https://www.pinterest.com/',
        logo='pinterest.png'
    )
    TUMBLR = SocialNetworkRecord(
        social_network_name='Tumblr',
        base_url='https://www.tumblr.com/',
        logo='tumblr.png'
    )
    QUORA = SocialNetworkRecord(
        social_network_name='Quora',
        base_url='https://www.quora.com/',
        logo='quora.png'
    )
    STACK_OVERFLOW = SocialNetworkRecord(
        social_network_name='Stack Overflow',
        base_url='https://stackoverflow.com/',
        logo='stack_overflow.png'
    )
    GOODREADS = SocialNetworkRecord(
        social_network_name='Goodreads',
        base_url='https://www.goodreads.com/',
        logo='goodreads.png'
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
