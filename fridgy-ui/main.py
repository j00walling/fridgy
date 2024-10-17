from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from chatbot import FridgyBot
import json
from datetime import datetime

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

fridgy_bot = FridgyBot()  # Create a single instance

def get_bot():
    return fridgy_bot

# Logging function for all chat history
def log_conversation(user_query, bot_response):
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "user_query": user_query,
        "bot_response": bot_response
    }
    
    with open("conversation_log.json", "a") as log_file:
        json.dump(log_entry, log_file)
        log_file.write("\n")  # Add a newline for readability

# Retrieval function for chat
@app.get("/api/conversation_history")
async def get_conversation_history():
    try:
        with open("conversation_log.json", "r") as log_file:
            history = [json.loads(line) for line in log_file]
        return {"history": history}
    except FileNotFoundError:
        return {"history": []}
            
@app.post("/api/query")
async def process_query(query: Query, bot: FridgyBot = Depends(get_bot)):
    messages = [{'role': 'user', 'content': query.question}]
    response = bot.chat_complete_messages(messages, 0)
    
    # Log the conversation
    log_conversation(query.question, response)
    
    return {"response": response, "context": bot.context}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)