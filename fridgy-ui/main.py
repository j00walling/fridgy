from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from chatbot import FridgyBot

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

@app.post("/api/query")
async def process_query(query: Query, bot: FridgyBot = Depends(get_bot)):
    messages = [{'role': 'user', 'content': query.question}]
    response = bot.chat_complete_messages(messages, 0)
    return {"response": response, "context": bot.context}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)