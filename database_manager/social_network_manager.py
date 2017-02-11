QUERIES = {
    'create_social_networks_table':
        """
        CREATE TABLE IF NOT EXISTS social_networks
        (
          id INTEGER PRIMARY KEY,
          name VARCHAR(50) NOT NULL UNIQUE,
          base_url VARCHAR(200) NOT NULL UNIQUE,
          path_to_logo TEXT
        )
        """,
    'insert_social_network':
        """
        INSERT INTO social_networks
        VALUES
        (?, ?, ?)
        """
}
