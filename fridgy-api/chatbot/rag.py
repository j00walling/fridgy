import os
import pdfplumber
from dotenv import load_dotenv
import openai
from pinecone import Pinecone, ServerlessSpec
import io

load_dotenv()

# Define the main prompt for the assistant
MAIN_PROMPT = "I am Fridgy, your intelligent refrigerator assistant."

class FridgyRagger:
    def __init__(self):
        # Initialize OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.context = [{'role': 'system', 'content': MAIN_PROMPT}]
        
        # Initialize Pinecone client
        self.pinecone_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
        self.pinecone_client = Pinecone(api_key=self.pinecone_key)
        self.index_name = os.getenv("PINECONE_INDEX")
        self.index = self._initialize_pinecone_index()
        
    def _initialize_pinecone_index(self):
        # Check if the index already exists; if not, create it
        if self.index_name not in self.pinecone_client.list_indexes().names():
            self.pinecone_client.create_index(
                name=self.index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=self.pinecone_env)
            )
        return self.pinecone_client.Index(self.index_name)

    @staticmethod
    def extract_text_from_pdf(file: bytes) -> str:
        text = ""
        with pdfplumber.open(io.BytesIO(file)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    @staticmethod
    def chunk_text_with_strides(text: str, chunk_size: int = 1000, stride: int = 500) -> list:
        words = text.split()
        chunks = [
            ' '.join(words[i:i + chunk_size]) for i in range(0, len(words), stride)
            if i + chunk_size <= len(words)
        ]
        if len(words) % chunk_size != 0:
            chunks.append(' '.join(words[-chunk_size:]))
        return chunks

    def create_and_store_embeddings(self, chunks: list):
        for i, chunk in enumerate(chunks):
            response = openai.embeddings.create(input=chunk, model="text-embedding-ada-002")
            # Access the embedding data correctly from the response object
            embedding = response.data[0].embedding  # Use `response.data` to access the embeddings
            self.index.upsert([(str(i), embedding, {"text": chunk})])  # each embedding is stored with a unique ID


    def retrieve_relevant_chunks(self, query: str, top_k: int = 3) -> list:
        # Get the embedding for the query
        response = openai.embeddings.create(input=query, model="text-embedding-ada-002")
        query_embedding = response.data[0].embedding  # Correct way to access the embedding data
        # Query Pinecone with the embedding
        result = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        return [match['metadata']['text'] for match in result['matches']]

    from chatbot.prompts import MAIN_PROMPT  # Import the MAIN_PROMPT from prompts.py
    def get_augmented_prompt_with_context(self, relevant_chunks: list, query: str) -> str:
        augmented_prompt = f"'{query}' \n\n Uploded Receipes: \n\n'{' '.join(relevant_chunks)}'"
        return augmented_prompt
