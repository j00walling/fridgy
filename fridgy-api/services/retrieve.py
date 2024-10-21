# retrieve.py
import datetime
import sqlite3

from services.db import UserDB, InventoryDB

# example Database of items and their expiry information
expiry_database = {
    "milk": {"shelf_life": 7, "storage": "refrigerated"},
    "bread": {"shelf_life": 5, "storage": "room temperature"},
    "eggs": {"shelf_life": 28, "storage": "refrigerated"},
    "apples": {"shelf_life": 14, "storage": "refrigerated"},
    "canned soup": {"shelf_life": 730, "storage": "room temperature"},  # 2 years
    "frozen pizza": {"shelf_life": 180, "storage": "frozen"},  # 6 months
}

# Placeholder function
def retrieve_relevant_info(query, context):
    """
    This function retrieves relevant information based on user queries
    during a conversation context to support RAG (Retrieval-Augmented Generation).
    """
    # Placeholder implementation
    return f"Relevant info for query: {query[:20]}... Context length: {len(context)}"

def get_inventory_info(email: str) -> str:
    """
    INVENTORY MANAGEMENT
    This function gets inventory information for a user query.
    """
    # Connect to and setup sqlite DB 
    conn = sqlite3.connect('services/db/inventory.db')
    inventory_db = InventoryDB(conn.cursor())
    inventory_db.setup()

    return f"Inventory info for query: {inventory_db.get_inventory_for_user(email=email)}..."

def add_inventory_info(email: str, item: str, quantity: int, expiration_date: str) -> None:
    """
    INVENTORY MANAGEMENT
    This function adds a food item, quantity, and expiration date of a food item based on a user query.
    Only one set of an item, quantity, and expiration date can be added with each user query.
    """
    # Connect to and setup sqlite DB 
    conn = sqlite3.connect('services/db/inventory.db')
    inventory_db = InventoryDB(conn.cursor())
    inventory_db.setup()

    # Insert item, quantity, and expiration date into inventory
    inventory_db.insert_item(email=email, item=item, quantity=quantity, expiration_date=expiration_date)

def remove_inventory_info(email: str, item: str, quantity: int, expiration_date: str) -> None:
    """
    INVENTORY MANAGEMENT
    This function adds a food item, quantity, and expiration date of a food item based on a user query.
    Only one set of an item, quantity, and expiration date can be added with each user query.
    """
    # Connect to and setup sqlite DB 
    conn = sqlite3.connect('services/db/inventory.db')
    inventory_db = InventoryDB(conn.cursor())
    inventory_db.setup()

    # Insert item, quantity, and expiration date into inventory
    inventory_db.insert_item(email=email, item=item, quantity=quantity, expiration_date=expiration_date)


def get_expiry_info(query) -> str:
    """
    This function manages food expiry information based on user queries.
    """
    query = query.lower()
    
    # Check if the query matches any item in our database
    for item, info in expiry_database.items():
        # Case 1: User provides known food item, but does not specify expiration
        if item in query and 'expir' not in query:
            shelf_life = info["shelf_life"]
            storage = info["storage"]
            
            # Calculate expiry date
            today = datetime.date.today()
            expiry_date = today + datetime.timedelta(days=shelf_life)
            
            response = f"{item.capitalize()} typically lasts for {shelf_life} days when stored {storage}. "
            response += f"If purchased today, it would expire around {expiry_date.strftime('%B %d, %Y')}."
            
            return response
        
        # Case 2: User provides known food item, and provides expiration

    # Case 3: User provides unknown food item
    # return "I'm sorry, I don't have information about the expiry date for that item."

    # Case 4: User is not asking an inventory management / expiration related query
    return ""
