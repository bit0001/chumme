QUERIES = {
    'create_friends_social_networks_table':
        """
        CREATE TABLE IF NOT EXISTS friends_social_networks
        (
          friend_id INTEGER NOT NULL,
          social_network_id INTEGER NOT NULL,
          social_network_link TEXT NOT NULL,
          FOREIGN KEY (friend_id)
            REFERENCES friends(id)
            ON DELETE CASCADE,
          FOREIGN KEY (social_network_id)
            REFERENCES social_networks(id),
          PRIMARY KEY (friend_id, social_network_id)
        );
        """,
    'insert_friend_':
        """
        INSERT INTO friends_social_networks
        VALUES
        (?, ?, ?)
        """
}
