from services.retrieve import manage_inventory

fridgy_tools = [
    {
        "type": "function",
        "function": {
            "name": "manage_inventory",
            "description": "Select, update, insert, or remove into a table by SQL",
            "parameters": {
                "type": "object",
                "properties": {
                    "dml": {
                        "type": "string",
                        "description": f"""SQL statement to do Select, update, insert, or remove on a table,
                        the SQL should be written using the following database schema:
                        Table name: inventory
                        ####Columns Names and type:
                        user_id INTEGER PRIMARY KEY,
                        item TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        expiration_date DATE NOT NULL

                        #### For INSERT operations:
                        Use the following format to insert or update on conflict:
                        ```sql
                        INSERT INTO inventory (user_id, item, quantity, expiration_date) 
                        VALUES (<user_id>, '<item>', <quantity>, '<expiration_date>')
                        ON CONFLICT (user_id, item) 
                        DO UPDATE SET 
                            quantity = inventory.quantity + EXCLUDED.quantity, 
                        ```
                    
                        ####
                            """,
                    },

                },
                "required": ["dml"],
            }
        }
    },
]

available_functions = {
    "manage_inventory": manage_inventory,
}