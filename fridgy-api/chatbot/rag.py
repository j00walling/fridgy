import os
import pdfplumber
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import io
import openai

# Load environment variables
load_dotenv()

class FridgyRagger:
    def __init__(self):
        # Set API keys
        openai.api_key = os.getenv("OPENAI_API_KEY")
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX")
        
        if not openai.api_key or not pinecone_api_key or not self.index_name:
            raise ValueError("Ensure API keys and index name are set in environment variables.")
        
        # Initialize Pinecone client and index
        self.pinecone_client = Pinecone(api_key=pinecone_api_key)
        self.index = self._initialize_pinecone_index()

    def _initialize_pinecone_index(self):
        """Initializes or retrieves the Pinecone index."""
        if self.index_name not in self.pinecone_client.list_indexes().names():
            self.pinecone_client.create_index(
                name=self.index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=os.getenv("PINECONE_ENVIRONMENT"))
            )
        return self.pinecone_client.Index(self.index_name)

    @staticmethod
    def extract_text_from_pdf(file: bytes) -> str:
        """Extracts text from each page of a PDF file."""
        with pdfplumber.open(io.BytesIO(file)) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages)

    @staticmethod
    def chunk_text_with_strides(text: str, chunk_size: int = 1000, stride: int = 500) -> list:
        """Splits text into overlapping chunks for context retention."""
        words = text.split()
        return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), stride)]

    def create_and_store_embeddings(self, chunks: list):
        """Generates and stores embeddings for each text chunk in Pinecone."""
        for i, chunk in enumerate(chunks):
            embedding = openai.embeddings.create(input=chunk, model="text-embedding-ada-002").data[0].embedding
            self.index.upsert([(str(i), embedding, {"text": chunk})])

    def retrieve_relevant_chunks(self, query: str, top_k: int = 3) -> list:
        """Retrieves the top K most relevant chunks for a query."""
        query_embedding = openai.embeddings.create(input=query, model="text-embedding-ada-002").data[0].embedding
        result = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        return [match['metadata']['text'] for match in result['matches']]

    def get_augmented_prompt_with_context(self, relevant_chunks: list, query: str) -> str:
        """Constructs a query prompt with relevant text context."""
        return f"'{query}'\n\nUploaded Recipes:\n\n'{' '.join(relevant_chunks)}'"
