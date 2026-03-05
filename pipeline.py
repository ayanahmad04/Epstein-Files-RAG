import os
from pathlib import Path

# Import your functions
from ingestion.download import download_dataset
from ingestion.clean import clean_dataset
from splitter.chunk import create_chunks
from embed.embedding import embed_chunks


DATA_DIR = Path("data")
RAW_PATH = DATA_DIR / "raw.json"
CLEANED_PATH = DATA_DIR / "cleaned.json"
CHUNKS_PATH = DATA_DIR / "chunks.json"
CHROMA_DIR = "chroma_db"


def run_pipeline():
    print("\n🚀 Starting RAG Data Pipeline...\n")

    # ---------------------------------------
    # Step 1: Download Dataset
    # ---------------------------------------
    if not RAW_PATH.exists():
        print("📥 Step 1: Downloading dataset...")
        download_dataset(str(RAW_PATH))
    else:
        print("⏩ Skipping download (raw.json already exists)")

    # ---------------------------------------
    # Step 2: Clean Dataset
    # ---------------------------------------
    if not CLEANED_PATH.exists():
        print("\n🧹 Step 2: Cleaning dataset...")
        clean_dataset(str(RAW_PATH), str(CLEANED_PATH))
    else:
        print("⏩ Skipping cleaning (cleaned.json already exists)")

    # ---------------------------------------
    # Step 3: Create Chunks
    # ---------------------------------------
    if not CHUNKS_PATH.exists():
        print("\n✂️ Step 3: Creating chunks...")
        create_chunks(str(CLEANED_PATH), str(CHUNKS_PATH))
    else:
        print("⏩ Skipping chunking (chunks.json already exists)")

    # ---------------------------------------
    # Step 4: Embed into Chroma
    # ---------------------------------------
    print("\n🧠 Step 4: Embedding chunks into Chroma...")
    embed_chunks(
        input_path=str(CHUNKS_PATH),
        chroma_dir=CHROMA_DIR,
        reset_db=True
    )

    print("\n🎉 Pipeline completed successfully!")
    print("📁 Vector DB ready at:", CHROMA_DIR)
    print("\nYou can now start the API using:")
    print("uvicorn main:app --reload\n")


if __name__ == "__main__":
    run_pipeline()