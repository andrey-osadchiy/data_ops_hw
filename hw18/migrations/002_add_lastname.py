from yoyo import step

__depends__ = {"001_create_users"}

steps = [
    step(
        """
        ALTER TABLE users
        ADD COLUMN lastname VARCHAR(100);
        """,
        """
        ALTER TABLE users
        DROP COLUMN lastname;
        """
    )
]
