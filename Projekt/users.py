import sqlite3

class User:
    def __init__(self, username, firstname, lastname):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

    def to_db(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        sql = f"INSERT INTO users(username, firstname, lastname) VALUES ('{self.username}', '{self.firstname}', '{self.lastname}')"
        cursor.execute(sql)
        connection.commit()
        connection.close()

    @classmethod
    def from_db(cls, username):
        connection = sqlite3.connect("database.db") # Muss vorher angelegt werden.
        cursor = connection.cursor()
        sql = f"SELECT username FROM users WHERE username = {username}"
        cursor.execute(sql)
        row = cursor.fetchone()
        connection.close()
        return User(row[0], row[1], row[2])

