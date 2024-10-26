# retrieve.py
import datetime
from typing import Any, Dict
import psycopg2

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


def manage_inventory(dml: str) -> Dict[str, Any]:
    """
    INVENTORY MANAGEMENT
    This function selects, updates, inserts, or removes food items with a quantity and expiration date for a user query.
    """
    try:
        fridgy_db = psycopg2.connect(
            host="localhost",        # Adjust if necessary
            user="rick",         # Your PostgreSQL username
            password="rick",     # Your PostgreSQL password
            database="fridgy"      # Your database name
        # Automatically commit after every transaction
        )
        # Enable autocommit mode
        fridgy_db.autocommit = True
        print("Database connection successful!")
    except Exception as e:
        print(f"Error: {e}")

    cursor = fridgy_db.cursor()

    error_code = 0
    result = None

    try:
        # Assuming you have an active connection and cursor
        cursor.execute(dml)

        # Only fetch results for SELECT queries
        if dml.strip().lower().startswith('select'):
            result = cursor.fetchall()
        else:
            result = None

        # Commit the transaction for DML queries like INSERT, UPDATE, DELETE
        fridgy_db.commit()
        print("SQL commit command completed...")

    except (Exception, psycopg2.Error) as e:
        print("Error while executing DML in PostgreSQL", e)
        error_code = 1

    final_res = {"code": error_code, "res": result}

    return final_res


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
