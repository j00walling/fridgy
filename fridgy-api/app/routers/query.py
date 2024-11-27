from fastapi import APIRouter, Depends, Form, File, UploadFile
from pydantic import BaseModel
from chatbot.bot import FridgyBot
from typing import Optional
from chatbot.rag import FridgyRagger
from chatbot.clip import FridgyClipper
from fastapi.responses import JSONResponse
import json

router = APIRouter()

class Query(BaseModel):
    question: str
    # user_id: int | None = None
    user_id: Optional[int] = None

fridgy_bot = FridgyBot()

# Initialize the FridgyRagger
fridgy_ragger = FridgyRagger()
fridgy_clipper = FridgyClipper()

def get_bot():
    return fridgy_bot

@router.post("/api/query")
async def process_query(query: Query, bot: FridgyBot = Depends(get_bot)):

    print(f"process_query <= {query}")

    messages = [{'role': 'user', 'content': query.question}]
    response = fridgy_bot.chat_complete_messages(messages, user_id=query.user_id)
    return {"response": response, "context": bot.context}


file_uploaded = False
image_uploaded = False
# Removed global variable and any file-specific state management.
@router.post("/api/upload_pdf")
async def upload_pdf(query: str = Form(...), file: UploadFile = File(...), bot: FridgyBot = Depends(get_bot)):

    global file_uploaded

    # Parse the JSON-formatted query string to Query object
    query_obj = Query(**json.loads(query))

    print(f"upload_pdf <= {query_obj}")

    if not file_uploaded:
        pdf_content = await file.read()
        text = fridgy_ragger.extract_text_from_pdf(pdf_content)
        chunks = fridgy_ragger.chunk_text_with_strides(text, chunk_size=1000, stride=500)
        fridgy_ragger.create_and_store_embeddings(chunks)
        file_uploaded = True

    relevant_chunks = fridgy_ragger.retrieve_relevant_chunks(query_obj)
    augmented_prompt = fridgy_ragger.get_augmented_prompt_with_context(relevant_chunks, query_obj)

    messages = [
        {'role': 'user', 'content': augmented_prompt},
    ]

    response = fridgy_bot.chat_complete_messages(messages, user_id=query_obj.user_id, process_raw = True)
    return {"response": response, "context": bot.context}

from PIL import Image
import io
@router.post("/api/upload_image")
async def upload_image(query: str = Form(...), file: UploadFile = File(...), bot: FridgyBot = Depends(get_bot)):

    global image_uploaded

    # Parse the JSON-formatted query string to Query object
    query_obj = Query(**json.loads(query))

    print(f"upload_image <= {query_obj}")

    image = Image.open(io.BytesIO(await file.read())).convert("RGB")

    augmented_prompt = fridgy_clipper.identify_grocery_items(image)

    messages = [
        {'role': 'user', 'content': augmented_prompt},
    ]

    print(f"image_uploaded => {messages}")

    response = fridgy_bot.chat_complete_messages(messages, user_id=query_obj.user_id, process_raw = True)
    return {"response": response, "context": bot.context}
