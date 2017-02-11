QUERIES = {
    'create_social_networks_table':
        """
        CREATE TABLE IF NOT EXISTS social_networks
        (
          id INTEGER PRIMARY KEY,
          social_network_name VARCHAR(50) NOT NULL UNIQUE,
          base_url VARCHAR(200) NOT NULL UNIQUE,
          logo_path TEXT
        )
        """,
    'insert_social_network':
        """
        INSERT INTO social_networks
        (social_network_name, base_url, logo_path)
        VALUES
        (?, ?, ?)
        """
}
