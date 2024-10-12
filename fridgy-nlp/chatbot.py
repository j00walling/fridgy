from dotenv import load_dotenv
from openai import OpenAI

from prompts import MAIN_PROMPT

class FridgyBot:
  def __init__(self):
    self.client = OpenAI()

  def converse(self) -> None:

    # Initialize chatbot
    chatContext = [
      {'role':'system', 'content': MAIN_PROMPT},
    ]

    response_message_content = self.chat_complete_messages(chatContext, 0)
    print("ChatBot: ", response_message_content)

    chatContext.append({'role': 'assistant', 'content': f"{response_message_content}"})

    # Chatbot-User conversation
    while True:
      # User input
      user_query = input("User Input: ")

      if user_query.lower() == "exit":
        print("ChatBot: Goodbye!")
        return
      
      # TODO: RAG OPERATIONS
      # TODO: Add inventory management to user query

      # TODO: Implement conversation flow with LangChain, LangGraph

      chatContext.append({'role': 'user', 'content': user_query})

      # Chatbot response
      response_message_content = self.chat_complete_messages(chatContext, 0)
      print("ChatBot: ", response_message_content)

      chatContext.append({'role': 'assistant', 'content': f"{response_message_content}"})

  def chat_complete_messages(self, messages, temperature) -> str:
    
    # query against the model "gpt-3.5-turbo-1106"
    completion = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages= messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
  fridgy = FridgyBot()
  fridgy.converse()