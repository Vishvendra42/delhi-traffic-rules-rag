import json
import faiss
from sentence_transformers import SentenceTransformer

INPUT_FILE = "data/delhi/processed/delhi_chunks.json"
OUTPUT_INDEX = "data/delhi/processed/delhi_faiss_index.idx"

MODEL_NAME = "all-MiniLM-L6-v2"


def main():
    # Load chunks
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [item["text"] for item in data]

    # Load embedding model
    model = SentenceTransformer(MODEL_NAME)

    # Convert text into vectors
    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings to FAISS
    index.add(embeddings)

    # Save index
    faiss.write_index(index, OUTPUT_INDEX)

    print(f"Created {len(embeddings)} embeddings")
    print(f"Embedding dimension: {dimension}")
    print(f"Saved FAISS index to: {OUTPUT_INDEX}")


if __name__ == "__main__":
    main()