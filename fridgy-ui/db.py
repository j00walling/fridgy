import sqlite3
from typing import List

class UserDB:
    def __init__(self, cursor):
        self.cursor = cursor

    def setup(self) -> None:
        """ 
        Create User DB table if it does not already exist for user authentication for Fridgy
        """

        try:
            # Specify User DB table schema
            TABLE_SQL = "CREATE TABLE IF NOT EXISTS USERS(username TEXT PRIMARY KEY, password TEXT NOT NULL);"

            # Create User table
            self.cursor.execute(TABLE_SQL)
        
        except sqlite3.Error as e:
            print(f"SQLite error encountered during table creation: {e}")

    def get_users(self) -> List[str]:
        """ 
        Retrieves all users authorized to access Fridgy
        """
        
        try:
            SELECT_SQL = f"SELECT username FROM USERS"
            users = self.cursor.execute(SELECT_SQL)
            return [user[0] for user in users]
        
        except sqlite3.Error as e:
            print(f"SQLite error encountered in selection: {e}")

    
    def insert_user(self, username: str, password: str) -> None:
        """
        Inserts username and password of a user using Fridgy
        """

        try:
            INSERT_SQL = f"INSERT OR REPLACE INTO USERS VALUES ('{username}', '{password}')"
            self.cursor.execute(INSERT_SQL)
        
        except sqlite3.Error as e:
            print(f"SQLite error encountered in insertion: {e}")


def user_db_main():
    """ Example User DB insertion and retrieval """

    try:
        # Connect to sqlite DB 
        conn = sqlite3.connect('user.db')

        # UserDB Client to insert and retriever user information from User DB
        user_db = UserDB(conn.cursor())
        user_db.setup()                     # Create User DB table if one doesn't already exist

        print(f"Users before insertion: {user_db.get_users()}")

        # Insert user and password
        user_db.insert_user("rick.truong@sjsu.edu", "rickpw1")
        
        print(f"Users after insertion: {user_db.get_users()}")

        # Save changes in User DB for persistence
        conn.commit()
    
    except sqlite3.Error as e:
        print(f"SQLite error encountered: {e}")

    finally:
        # Close User DB connection
        conn.close()


if __name__ == "__main__":
    user_db_main()




# def example():
#     try:
#         # Connecting to sqlite 
#         conn = sqlite3.connect('user.db') 

#         # Creating a cursor object using the 
#         # cursor() method 
#         cursor = conn.cursor() 

#         # Creating table 
#         TABLE_SQL = "CREATE TABLE USERS(username TEXT, password TEXT);"
#         cursor.execute(TABLE_SQL) 

#         # Queries to INSERT records. 
#         cursor.execute('''INSERT INTO USERS VALUES ('rick.truong@sjsu.edu', 'pw1')''') 
#         cursor.execute('''INSERT INTO USERS VALUES ('person@sjsu.edu', 'pw2')''') 

#         # Display data inserted 
#         print("Data Inserted in the table: ") 
#         data=cursor.execute('''SELECT * FROM USERS''') 
#         for row in data:
#             print(row)

#         # Commit your changes in the database	 
#         conn.commit() 
    
#     except sqlite3.Error as e:
#         print(f"SQLite error encountered: {e}")

#     finally:
#         # Closing the connection 
#         conn.close()
