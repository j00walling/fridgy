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
                        email TEXT PRIMARY KEY,
                        item TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        expiration_date TEXT NOT NULL
                    );

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