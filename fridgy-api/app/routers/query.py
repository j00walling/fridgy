from fastapi import APIRouter, Depends
from pydantic import BaseModel
from chatbot.bot import FridgyBot


router = APIRouter()

class Query(BaseModel):
    question: str
    user_id: int | None = None

fridgy_bot = FridgyBot()

def get_bot():
    return fridgy_bot

@router.post("/api/query")
async def process_query(query: Query, bot: FridgyBot = Depends(get_bot)):
    messages = [{'role': 'user', 'content': query.question}]
    response = fridgy_bot.chat_complete_messages(messages, user_id=query.user_id)
    return {"response": response, "context": bot.context}
