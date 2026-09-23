import json
import faiss
from sentence_transformers import SentenceTransformer


INDEX_FILE = "data/delhi/processed/delhi_faiss_index.idx"
CHUNKS_FILE = "data/delhi/processed/delhi_chunks.json"

MODEL_NAME = "all-MiniLM-L6-v2"


class Retriever:

    def __init__(self):
        # Load FAISS index
        self.index = faiss.read_index(INDEX_FILE)

        # Load chunks
        with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        # Load embedding model
        self.model = SentenceTransformer(MODEL_NAME)

    def search(self, query, top_k=5):

        # Convert question into embedding
        query_embedding = self.model.encode([query])

        # Search similar chunks
        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for i in indices[0]:
            if i < len(self.chunks):
                results.append(self.chunks[i])

        return results