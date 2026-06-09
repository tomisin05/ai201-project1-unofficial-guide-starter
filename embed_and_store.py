"""
embed_and_store.py — Embed all chunks from ingest.py and store them in ChromaDB.

Run with:  python embed_and_store.py
"""

import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, clean_text, chunk_text

COLLECTION_NAME = "gmu_student_leadership"
CHROMA_DIR = "chroma_db"


def build_vector_store():
    # ── Load, clean, and chunk all documents ──────────────────────────────────
    print("=== Loading and chunking documents ===")
    raw_docs = load_documents("documents")
    all_chunks = []
    for doc in raw_docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned, source=doc["source"])
        all_chunks.extend(chunks)
    print(f"Total chunks to embed: {len(all_chunks)}\n")

    # ── Embed ──────────────────────────────────────────────────────────────────
    print("=== Embedding with all-MiniLM-L6-v2 ===")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    print()

    # ── Store in ChromaDB ──────────────────────────────────────────────────────
    print("=== Storing in ChromaDB ===")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Drop and recreate so re-runs don't duplicate
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(COLLECTION_NAME)

    collection.add(
        ids=[f"chunk_{i}" for i in range(len(all_chunks))],
        embeddings=[e.tolist() for e in embeddings],
        documents=texts,
        metadatas=[
            {"source": c["source"], "chunk_index": i}
            for i, c in enumerate(all_chunks)
        ],
    )

    print(f"Stored {collection.count()} chunks in '{COLLECTION_NAME}'.")
    print(f"ChromaDB persisted to ./{CHROMA_DIR}/\n")


if __name__ == "__main__":
    build_vector_store()