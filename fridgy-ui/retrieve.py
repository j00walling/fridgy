# retrieve.py
import datetime

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

# Placeholder function
def get_inventory_info(query):
    """
    This function manages inventory information based on user queries.
    """
    # Placeholder implementation
    return f"Inventory info for query: {query[:20]}..."


def get_expiry_info(query):
    """
    This function manages expiry information based on user queries.
    """
    query = query.lower()
    
    # Check if the query matches any item in our database
    for item, info in expiry_database.items():
        if item in query:
            shelf_life = info["shelf_life"]
            storage = info["storage"]
            
            # Calculate expiry date
            today = datetime.date.today()
            expiry_date = today + datetime.timedelta(days=shelf_life)
            
            response = f"{item.capitalize()} typically lasts for {shelf_life} days when stored {storage}. "
            response += f"If purchased today, it would expire around {expiry_date.strftime('%B %d, %Y')}."
            
            return response
    
    # If no match found
    return "I'm sorry, I don't have information about the expiry date for that item."