import sqlite3
   

class Transaction:
    def __init__(self, sending_username, receiving_username, transaction_amount):
        self.sending_username = sending_username
        self.receiving_username = receiving_username
        self.transaction_amount = transaction_amount
        
    #Transfer wird in Datenbank zwischengespeichert
    def to_db(self):
        try:
            # Establish a connection to the SQLite database
            connection = sqlite3.connect("./database.db")
            # Create a cursor object to interact with the database
            cursor = connection.cursor()
            sql = "INSERT INTO transactions (sending_username, receiving_username, transaction_amount) VALUES (?, ?, ?)"
            cursor.execute(sql, (self.sending_username, self.receiving_username, self.transaction_amount))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in _query: {e}")
        finally:
            if connection:
                connection.close()