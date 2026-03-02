from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            birthdate DATE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """,
        """
        DROP TABLE users;
        """
    )
]
