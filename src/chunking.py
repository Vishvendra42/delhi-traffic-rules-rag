import json
import re

INPUT_FILE = "data/delhi/raw/MASTER_DELHI_TRAFFIC_KNOWLEDGE_BASE.txt"
OUTPUT_FILE = "data/delhi/processed/delhi_chunks.json"

CHUNK_SIZE = 2000
OVERLAP = 300


def clean_text(text):
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def create_chunks(text):
    chunks = []

    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - OVERLAP

    return chunks


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    text = clean_text(text)

    chunks = create_chunks(text)

    data = []

    for i, chunk in enumerate(chunks):

        data.append({
            "chunk_id": i,
            "source": "Delhi Traffic Master Knowledge Base",
            "jurisdiction": "Delhi",
            "text": chunk
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Created {len(data)} chunks")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()