import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from chatbot.prompts import MAIN_PROMPT  # Main prompt used for chatbot initialization
from services.retrieve import *
from chatbot.tools import fridgy_tools, available_functions
import pprint

# Load environment variables from .env file
load_dotenv()

class FridgyBot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize the bot's context with MAIN_PROMPT
        self.context = [{'role': 'system', 'content': MAIN_PROMPT}]
        self.tools = fridgy_tools

    def chat_complete_messages(self, messages, user_id: int = None, process_raw=False) -> str:
        pprint.pprint(f"chat_complete_messages (raw) <= {messages}")
        
        user_query = messages[-1]['content']
        augmented_query = f"{user_query}"

        # Combine stored context with new messages
        full_context = self.context + messages
        
        if not process_raw:
            # Retrieve additional context about expiry dates if applicable
            expiry_info = get_expiry_info(user_query)
            augmented_query += f"\n\nAdditional context: {expiry_info}"

        augmented_query += f"\n\nUser ID: {user_id}"

        # Update the user's last message with the augmented query
        full_context[-1]['content'] = augmented_query

        pprint.pprint(f"chat_complete_messages (augmented) <= {full_context}")

        # Request response from OpenAI API
        response = self.chat_completion_request(full_context, tools=self.tools, tool_choice="auto")
        assistant_message = response.choices[0].message

        tool_calls = assistant_message.tool_calls
        print(f"tool calls: {tool_calls}")
        print("Fridgy:", assistant_message.content)

        # Update context based on whether tools are used in the response
        if not tool_calls:
            self.context.extend([
                {'role': 'user', 'content': user_query},
                {'role': 'assistant', 'content': f"{assistant_message}"}
            ])
        else:
            # Handle tool calls if present in the assistant's response
            self.context.append(assistant_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                print("function_args:", function_args)

                # Execute tool call and handle the response
                function_response = function_to_call(dml=function_args.get("dml"))
                if function_response["code"] != 0:
                    function_message = "Something went wrong while querying the database"
                else:
                    function_message = f"Database query was successful! The following was returned: {function_response['res']}"

                self.context.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_message,
                })

            # Fetch the final response after tool interactions
            response = self.chat_completion_request(self.context, tools=self.tools, tool_choice="auto")
            self.context.extend([
                {'role': 'user', 'content': user_query},
                {'role': 'assistant', 'content': response.choices[0].message.content}
            ])

        # Limit context size to manage memory usage effectively
        max_context_length = 1024
        if len(self.context) > max_context_length:
            self.context = self.context[-max_context_length:]

        return response

    def chat_completion_request(self, messages, temperature=0, tools=None, tool_choice=None, model='gpt-4-1106-preview'):
        try:
            return self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                tools=tools,
                tool_choice=tool_choice,
            )
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e
