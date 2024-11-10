import os
import pdfplumber
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import io
import openai

# Load environment variables from .env file
load_dotenv()

class FridgyRagger:
    def __init__(self):
        # Set OpenAI API key
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found. Ensure OPENAI_API_KEY is set in the environment variables.")
        
        # Initialize Pinecone client and set up index
        self.pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX")
        self.index = self._initialize_pinecone_index()

    def _initialize_pinecone_index(self):
        """Creates a Pinecone index if it doesn't exist and returns the index object."""
        if self.index_name not in self.pinecone_client.list_indexes().names():
            # Define index with specified dimensions and similarity metric
            self.pinecone_client.create_index(
                name=self.index_name,
                dimension=1536,  # Embedding dimension for OpenAI's Ada model
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=os.getenv("PINECONE_ENVIRONMENT"))
            )
        return self.pinecone_client.Index(self.index_name)

    @staticmethod
    def extract_text_from_pdf(file: bytes) -> str:
        """Extracts and concatenates text from each page of a PDF."""
        with pdfplumber.open(io.BytesIO(file)) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages)

    @staticmethod
    def chunk_text_with_strides(text: str, chunk_size: int = 1000, stride: int = 500) -> list:
        """Splits text into overlapping chunks to retain context between parts."""
        words = text.split()
        # Create chunks of specified size with overlap defined by stride
        chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), stride)]
        # Ensure the last chunk includes any remaining words
        return chunks if len(words) % chunk_size == 0 else chunks + [' '.join(words[-chunk_size:])]

    def create_and_store_embeddings(self, chunks: list):
        """Generates and stores embeddings in Pinecone for each text chunk."""
        for i, chunk in enumerate(chunks):
            # Generate embedding for the chunk and store in Pinecone with unique ID and metadata
            embedding = openai.embeddings.create(input=chunk, model="text-embedding-ada-002").data[0].embedding
            self.index.upsert([(str(i), embedding, {"text": chunk})])

    def retrieve_relevant_chunks(self, query: str, top_k: int = 3) -> list:
        """Retrieves the top K most relevant text chunks for a given query."""
        # Generate embedding for the query
        query_embedding = openai.embeddings.create(input=query, model="text-embedding-ada-002").data[0].embedding
        # Query Pinecone for closest matches and extract the text metadata
        result = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        return [match['metadata']['text'] for match in result['matches']]

    def get_augmented_prompt_with_context(self, relevant_chunks: list, query: str) -> str:
        """Constructs a prompt that includes the query and relevant context from text chunks."""
        return f"'{query}' \n\n Uploaded Recipes: \n\n'{' '.join(relevant_chunks)}'"
