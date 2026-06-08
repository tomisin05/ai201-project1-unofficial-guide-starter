"""
ingest.py — Document loading, cleaning, and chunking for the GMU Student Leadership RAG pipeline.

Run with:  python ingest.py
"""

import os
import re
import csv
import random

DOCUMENTS_DIR = "documents"
CHUNK_SIZE = 500       # characters
OVERLAP = 50           # characters
SKIP_FILES = {".gitkeep"}


# ── 1. LOADING ────────────────────────────────────────────────────────────────

def load_plain_text(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_csv_as_text(filepath: str) -> str:
    """Convert each CSV row into a readable sentence so it chunks like prose."""
    sentences = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Organization Name", "").strip()
            category = row.get("Main Category", "").strip()
            subcategories = row.get("Subcategories", "").strip()
            duration = row.get("Membership Duration", "").strip()
            if name:
                sentence = f"{name} is a {category}"
                if subcategories:
                    sentence += f" in the following categories: {subcategories}"
                if duration:
                    sentence += f". Membership lasts: {duration}."
                sentences.append(sentence)
    return "\n".join(sentences)


def load_documents(directory: str) -> list[dict]:
    """
    Returns a list of dicts: {"source": filename, "text": raw_text}
    Skips empty files and non-text files.
    """
    docs = []
    for filename in os.listdir(directory):
        if filename in SKIP_FILES:
            continue

        filepath = os.path.join(directory, filename)

        if filename.endswith(".csv"):
            text = load_csv_as_text(filepath)
        else:
            text = load_plain_text(filepath)

        if not text.strip():
            print(f"  [skip] {filename} — empty after loading")
            continue

        docs.append({"source": filename, "text": text})
        print(f"  [loaded] {filename} ({len(text)} chars)")

    return docs


# ── 2. CLEANING ───────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Decode common HTML entities
    text = text.replace("&amp;", "&").replace("&nbsp;", " ").replace("&lt;", "<") \
               .replace("&gt;", ">").replace("&#39;", "'").replace("&quot;", '"')
    # Collapse runs of whitespace / blank lines into a single newline
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


# ── 3. CHUNKING ───────────────────────────────────────────────────────────────

def chunk_text(text: str, source: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[dict]:
    """
    Splits text into overlapping character-level chunks.
    Returns a list of dicts: {"source": ..., "text": chunk_text}
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 0:
            chunks.append({"source": source, "text": chunk})
        start += chunk_size - overlap  # slide forward with overlap
    return chunks


# ── 4. MAIN ───────────────────────────────────────────────────────────────────

def main():
    print("=== Loading documents ===")
    raw_docs = load_documents(DOCUMENTS_DIR)
    print(f"\nLoaded {len(raw_docs)} documents.\n")

    print("=== Cleaning and chunking ===")
    all_chunks = []
    for doc in raw_docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned, source=doc["source"])
        all_chunks.extend(chunks)
        print(f"  {doc['source']}: {len(chunks)} chunks")

    print(f"\nTotal chunks: {len(all_chunks)}")

    print("\n=== 5 random chunks (spot-check) ===\n")
    sample = random.sample(all_chunks, min(5, len(all_chunks)))
    for i, chunk in enumerate(sample, 1):
        print(f"--- Chunk {i} | source: {chunk['source']} ---")
        print(chunk["text"])
        print()


if __name__ == "__main__":
    main()
