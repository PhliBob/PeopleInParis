import sqlite3

class User:
    def __init__(self, username, firstname, lastname, password, amount, isLoggedIn):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.amount = amount
        
        self.isLoggedIn = isLoggedIn

# Benutzer in Datenbank speichern
    
    def to_db(self):
        try:
            
            connection = sqlite3.connect("./database.db")
            
            cursor = connection.cursor()
            
            sql = "INSERT INTO users (username, firstname, lastname, password, amount, isLoggedIn) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, (self.username, self.firstname, self.lastname, self.password, self.amount, 0))
            
            connection.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in _query: {e}")
        finally:
            
            if connection:
                connection.close()

    
#Ruft benutzer aus Datenbank raus
                
    @classmethod
    def from_db(cls, username):
        try:
            connection = sqlite3.connect("./database.db")
            cursor = connection.cursor()
            sql = "SELECT username, firstname, lastname, password, amount, isLoggedIn FROM users WHERE username = ?"
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            if row:
                return cls(row[0], row[1], row[2], row[3], row[4], row[5])
            else:
                print("User not found")
                return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        except Exception as e:
            print(f"Exception in _query: {e}")
            return None
        finally:
            if connection:
                connection.close()

#"isloggedin" wird auf True gesetzt
                
    @classmethod
    def login(cls, username):
        try:
            connection = sqlite3.connect("./database.db")
            cursor = connection.cursor()
            sql = "UPDATE users SET isLoggedIn = 1 WHERE username = ?"
            cursor.execute(sql, (username,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in _query: {e}")
        finally:
            if connection:
                connection.close()

#"isloggedin" wird auf False gesetzt
                
    @classmethod
    def logout(cls, username):
        try:
            connection = sqlite3.connect("./database.db")
            cursor = connection.cursor()
            sql = "UPDATE users SET isLoggedIn = 0 WHERE username = ?"
            cursor.execute(sql, (username,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in _query: {e}")
        finally:
            if connection:
                connection.close()
    
#Balance wird geupdated
                
    @classmethod
    def update_amount(cls, username, new_amount):
        try:
            connection = sqlite3.connect("./database.db")
            cursor = connection.cursor()
            sql = "UPDATE users SET amount = ? WHERE username = ?"
            cursor.execute(sql, (new_amount, username))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in _query: {e}")
        finally:
            if connection:
                connection.close()
        
    @classmethod
    def get_logged_in_user(cls):
        try:
            connection = sqlite3.connect("./database.db")
            cursor = connection.cursor()
            sql = "SELECT username, firstname, lastname, password, amount, isLoggedIn FROM users WHERE isLoggedIn = 1"
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return cls(*row)
            else:
                print("No user currently logged in")
                return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        except Exception as e:
            print(f"Exception in get_logged_in_user: {e}")
            return None
        finally:
            if connection:
                connection.close()