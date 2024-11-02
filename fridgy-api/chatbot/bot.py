import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from chatbot.prompts import MAIN_PROMPT  # Import the MAIN_PROMPT from prompts.py
from services.retrieve import *
from chatbot.tools import fridgy_tools, available_functions

load_dotenv()

class FridgyBot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize the context with MAIN_PROMPT as the first message
        self.context = [{'role': 'system', 'content': MAIN_PROMPT}]
        self.tools = fridgy_tools

    def chat_complete_messages(self, messages, user_id: int = None, process_raw = False) -> str:

        print(f"chat_complete_messages (messages) <= ${messages}")

        user_query = messages[-1]['content']

        # Combine stored context with new messages
        full_context = self.context + messages
        
        if not process_raw:
            # Check if the query is about expiration dates
            expiry_info = get_expiry_info(user_query)

            # # Function for retrieving previous chat context for a user
            # # Use the retrieve module to call these functions
            # relevant_info = retrieve.retrieve_relevant_info(user_query, full_context)
            # inventory_info = get_inventory_info(user_email)

            # Augment the user's query with relevant information
            augmented_query = f"{user_query}\n\nAdditional context: {expiry_info}\n\nUser ID: {user_id}"

            # Replace the user's query in the last message with the augmented query
            full_context[-1]['content'] = augmented_query

        print(f"chat_complete_messages <= {full_context}")
        
        # Call the OpenAI API to get a completion
        response = self.chat_completion_request(full_context, 0, tools=fridgy_tools, tool_choice="auto")
        assistant_message = response.choices[0].message

        tool_calls = assistant_message.tool_calls
        print(f"tool calls: {tool_calls}")
        print("Fridgy: ", assistant_message.content)


        # Update the context with the user message and the assistant's response
        if not tool_calls:
            self.context.append({'role': 'user', 'content': user_query})
            self.context.append({'role': 'assistant', 'content': f"{assistant_message}"})
        
        else:
            # Step 3: call the function.
            self.context.append(assistant_message)

            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                #print("GPT to call! function: ", function_name)
                #print("function name is: ", function_name)
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                print("function_args:", function_args)

                function_response = function_to_call(
                    dml = function_args.get("dml")
                )

                if function_response["code"] != 0:
                    function_message = "Something went wrong while querying the database"
                else:
                    function_message = f"Database query was successful! The following was returned: {function_response['res']}"

                self.context.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_message,
                    }
                )
            
            response = self.chat_completion_request(self.context, temperature=0, tools=fridgy_tools, tool_choice="auto")
            self.context.append({'role': 'user', 'content': user_query})
            self.context.append({'role': 'assistant', 'content': response.choices[0].message.content})

        # Limit the context size to prevent it from growing too large
        max_context_length = 10  # Adjust as needed
        if len(self.context) > max_context_length:
            self.context = self.context[-max_context_length:]

        return response

    def chat_completion_request(self, messages, temperature=0, tools=None, tool_choice=None, model='gpt-4-1106-preview'):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                tools=tools,
                tool_choice=tool_choice,
            )
            return response
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e