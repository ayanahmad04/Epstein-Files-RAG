import json
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter

def hash_text(t):
    return hashlib.sha256(t.lower().encode()).hexdigest()

def create_chunks(input_path="data/cleaned.json",
                  output_path="data/chunks.json",
                  chunk_size=1200,
                  overlap=150):

    with open(input_path, "r", encoding="utf-8") as f:
        docs = json.load(f)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )

    seen = set()
    chunks = []

    for d in docs:
        parts = splitter.split_text(d["text"])
        for i, p in enumerate(parts):
            key = hash_text(p)
            if key in seen:
                continue
            seen.add(key)

            chunks.append({
                "text": p,
                "metadata": {
                    "source": d["file"],
                    "chunk": i
                }
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print("Total chunks:", len(chunks))