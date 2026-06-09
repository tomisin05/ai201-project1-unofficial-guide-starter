"""
generate.py — Grounded answer generation using Groq + retrieved chunks.

The system prompt hard-enforces grounding: the model is only allowed to answer
from the provided context. If the context doesn't cover the question, it must say so.
"""

import os
from groq import Groq
from dotenv import load_dotenv
from retrieve import retrieve

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a helpful assistant for students at George Mason University who want to learn about student leadership, student organizations, and student government.

Answer the user's question using ONLY the information provided in the context below. Do not use any outside knowledge or information from your training data. Every claim in your answer must be traceable to the provided context.

If the context does not contain enough information to answer the question, respond with exactly: "I don't have enough information in my documents to answer that."

Be specific and direct. Do not pad your answer with generic advice."""


def ask(question: str, k: int = 5) -> dict:
    """
    Retrieves relevant chunks, sends them to Groq, and returns a grounded answer.

    Returns:
        {
            "answer": str,
            "sources": list[str],   # deduplicated source filenames
            "chunks": list[dict],   # full retrieved chunks for inspection
        }
    """
    chunks = retrieve(question, k=k)

    # Build context block — each chunk labeled with its source
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(f"[{i}] (source: {chunk['source']})\n{chunk['text']}")
    context = "\n\n".join(context_parts)

    user_message = f"""Context:
{context}

Question: {question}"""

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,  # low temp = more faithful to context
    )

    answer = response.choices[0].message.content.strip()

    # Programmatically collect sources — don't rely on the LLM to do this
    sources = list(dict.fromkeys(chunk["source"] for chunk in chunks))

    return {"answer": answer, "sources": sources, "chunks": chunks}


if __name__ == "__main__":
    test_questions = [
        "How many seats are in the Undergraduate Representative Body and how are they distributed?",
        "What resources does an RSO get after registering with Student Involvement?",
        "What is the best pizza place near campus?",  # out-of-scope — should decline
    ]

    for question in test_questions:
        print(f"Q: {question}")
        print("-" * 70)
        result = ask(question)
        print(f"A: {result['answer']}")
        print(f"\nSources: {', '.join(result['sources'])}")
        print("=" * 70)
        print()
