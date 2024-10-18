import sqlite3
from typing import List


class UserDB:
    """
    USER DATABASE FOR AUTHENTICATION
    """
    
    def __init__(self, cursor):
        self.cursor = cursor

    def setup(self) -> None:
        """ 
        Create User DB table if it does not already exist for user authentication for Fridgy
        """

        try:
            # Specify User DB table schema
            TABLE_SQL = "CREATE TABLE IF NOT EXISTS USERS(email TEXT PRIMARY KEY, password TEXT NOT NULL);"

            # Create User table
            self.cursor.execute(TABLE_SQL)
        
        except sqlite3.Error as e:
            print(f"SQLite error encountered during table creation: {e}")

    def get_users(self) -> List[str]:
        """ 
        Retrieves all users authorized to access Fridgy
        """
        
        try:
            SELECT_SQL = f"SELECT email FROM USERS"
            users = self.cursor.execute(SELECT_SQL)
            return [user[0] for user in users]
        
        except sqlite3.Error as e:
            print(f"SQLite error encountered in selection: {e}")

    
    def insert_user(self, email: str, password: str) -> None:
        """
        Inserts email and password of a user using Fridgy
        """

        try:
            INSERT_SQL = f"INSERT OR REPLACE INTO USERS VALUES ('{email}', '{password}')"
            self.cursor.execute(INSERT_SQL)
        
        except sqlite3.Error as e:
            print(f"SQLite error encountered in insertion: {e}")

class InventoryDB:
    """
    INVENTORY DATABASE FOR REFRIGERATOR
    """
    
    def __init__(self, cursor):
        self.cursor = cursor

    def setup(self) -> None:
        """ 
        Create Inventory DB table if it does not already exist for inventory management for Fridgy
        """

        try:
            # Specify User DB table schema
            TABLE_SQL = """CREATE TABLE IF NOT EXISTS INVENTORY(
email TEXT PRIMARY KEY,
item TEXT NOT NULL,
quantity INTEGER NOT NULL,
expiration_date TEXT NOT NULL
);"""

            # Create User table
            self.cursor.execute(TABLE_SQL)
        
        except sqlite3.Error as e:
            print(f"SQLite error encountered during table creation: {e}")

    def get_inventory_for_user(self, email: str) -> List[str]:
        """ 
        Retrieves refrigerator inventory of a user
        """
        
        try:
            SELECT_SQL = f"SELECT item, quantity, expiration_date FROM INVENTORY WHERE email == '{email}'"
            inventory = self.cursor.execute(SELECT_SQL)
            return list(inventory)
        
        except sqlite3.Error as e:
            print(f"SQLite error encountered in selection: {e}")

    
    def insert_item(self, email: str, item: str, quantity: int, expiration_date: str) -> None:
        """
        Inserts food item, quantity, and expiration of food item in refrigerator
        """

        try:
            INSERT_SQL = f"INSERT OR REPLACE INTO INVENTORY VALUES ('{email}', '{item}', '{quantity}', '{expiration_date}')"
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

def inventory_db_main():
    """ Example User DB insertion and retrieval """

    try:
        # Connect to sqlite DB 
        conn = sqlite3.connect('inventory.db')

        # UserDB Client to insert and retriever user information from User DB
        inventory_db = InventoryDB(conn.cursor())
        inventory_db.setup()                     # Create User DB table if one doesn't already exist

        print(f"""Inventory before insertion for @sjsu.edu: {inventory_db.get_inventory_for_user(email="")}""")

        # Insert user and password
        inventory_db.insert_item(email="rick.truong@sjsu.edu", item="eggs", quantity=1, expiration_date="10-18-24")
        inventory_db.insert_item(email="rick.truong@sjsu.edu", item="steak", quantity=10, expiration_date="10-28-24")

        print(f"""Inventory after insertion for rick.truong@sjsu.edu: {inventory_db.get_inventory_for_user(email="rick.truong@sjsu.edu")}""")

        # Save changes in User DB for persistence
        conn.commit()
    
    except sqlite3.Error as e:
        print(f"SQLite error encountered: {e}")

    finally:
        # Close User DB connection
        conn.close()


if __name__ == "__main__":
    # user_db_main()
    inventory_db_main()




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
