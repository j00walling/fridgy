from dotenv import load_dotenv
from openai import OpenAI
from prompts import MAIN_PROMPT  # Import the MAIN_PROMPT from prompts.py
import retrieve
import os

load_dotenv()

class FridgyBot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize the context with MAIN_PROMPT as the first message
        self.context = [{'role': 'system', 'content': MAIN_PROMPT}]

    def chat_complete_messages(self, messages, temperature) -> str:
        user_query = messages[-1]['content']
    
        # Combine stored context with new messages
        full_context = self.context + messages
        
        # # Function for retrieving previous chat context for a user
        # # Use the retrieve module to call these functions
        # relevant_info = retrieve.retrieve_relevant_info(user_query, full_context)
        # inventory_info = retrieve.get_inventory_info(user_query)
        
        # Augment the user's query with relevant information
        augmented_query = f"{user_query}"
        
        # Replace the user's query in the last message with the augmented query
        full_context[-1]['content'] = augmented_query
        
        # Call the OpenAI API to get a completion
        completion = self.client.chat.completions.create(
            model='gpt-4-1106-preview',
            messages=full_context,
            temperature=temperature,
        )
        response = completion.choices[0].message.content

        # Update the context with the user message and the assistant's response
        self.context.append({'role': 'user', 'content': user_query})
        self.context.append({'role': 'assistant', 'content': response})

        # Limit the context size to prevent it from growing too large
        max_context_length = 10  # Adjust as needed
        if len(self.context) > max_context_length:
            self.context = self.context[-max_context_length:]

        return response
