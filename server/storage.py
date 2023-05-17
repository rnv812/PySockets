import hashlib

from sqlite3 import connect, Connection


class Storage:
    def __init__(self, filename: str = 'storage.db') -> None:
        self._filename = filename

    def _get_connection(self) -> Connection:
        return connect(self._filename)

    def create_user(self, username: str, password: str) -> None:
        query = """
            INSERT INTO users (username, password, balance)
            VALUES (?, ?, ?)
        """
        hashed_password = Storage._hash_password(password)

        with self._get_connection() as connection:
            connection.execute(query, (username, hashed_password, 0.0))
            connection.commit()

    def authenticate(self, username: str, password: str) -> bool:
        query = """SELECT * FROM users WHERE username=? AND password=?"""
        hashed_password = Storage._hash_password(password)

        with self._get_connection() as connection:
            result = connection.execute(
                query,
                (username, hashed_password)
            ).fetchone()
            connection.commit()

        return result is not None

    def get_balance(self, username: str) -> float:
        query = """SELECT balance FROM users WHERE username=?"""

        with self._get_connection() as connection:
            result = connection.execute(query, (username, )).fetchone()

        return result[0]

    def update_balance(self, username: str, amount: float) -> None:
        query = """UPDATE users SET balance=? WHERE username=?"""

        with self._get_connection() as connection:
            connection.execute(query, (amount, username, ))
            connection.commit()

    def delete_user(self, username: str) -> None:
        query = """DELETE FROM users WHERE username=?"""

        with self._get_connection() as connection:
            connection.execute(query, (username, ))
            connection.commit()

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
