"""
retrieve.py — Query the ChromaDB vector store and inspect retrieval quality.

Run with:  python retrieve.py
"""

import chromadb
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "gmu_student_leadership"
CHROMA_DIR = "chroma_db"
TOP_K = 5

_model = None
_collection = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_collection(COLLECTION_NAME)
    return _collection


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """
    Returns the top-k most relevant chunks for a query.
    Each result: {"text": ..., "source": ..., "chunk_index": ..., "distance": ...}
    """
    model = _get_model()
    collection = _get_collection()

    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"] or [[]]
    metadatas = results["metadatas"] or [[]]
    distances = results["distances"] or [[]]

    output = []
    for text, meta, dist in zip(documents[0], metadatas[0], distances[0]):
        output.append({
            "text": text,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": round(dist, 4),
        })
    return output


# ── Evaluation test ───────────────────────────────────────────────────────────

TEST_QUERIES = [
    "How many seats are in the Undergraduate Representative Body and how are they distributed?",
    "What is the RSO HUB and what can you use it for?",
    "What resources does an RSO get after registering with Student Involvement?",
]

if __name__ == "__main__":
    for query in TEST_QUERIES:
        print(f"QUERY: {query}")
        print("-" * 70)
        chunks = retrieve(query)
        for i, chunk in enumerate(chunks, 1):
            print(f"  [{i}] source: {chunk['source']}  |  distance: {chunk['distance']}")
            print(f"       {chunk['text'][:300].replace(chr(10), ' ')}")
            print()
        print("=" * 70)
        print()
