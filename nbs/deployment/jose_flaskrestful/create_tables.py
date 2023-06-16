import sqlite3


class DBConnection:
    """Context manager for opening and closing data bases."""

    def __init__(self, database: str):
        self.database = database
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.database)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()


def create_tables():
    create_table_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
    create_table_items = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
    insert_item = "INSERT INTO items VALUES (?, ?)"

    with DBConnection("data.db") as cursor:
        cursor.execute(create_table_users)
        cursor.execute(create_table_items)
        cursor.execute(insert_item, ("chum", 5.99))


if __name__ == "__main__":
    create_tables()
