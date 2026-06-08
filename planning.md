# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Becoming a Student Leader at George Mason University

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #   | Source                                      | Description                                                                              | URL or location                                      |
| --- | ------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| 1   | GMU Student Government (About SG)           | Overview of GMU's Student Government structure, mission, elected/appointed roles         | documents/ABOUT_SG_GMU                               |
| 2   | GMU Undergraduate Representative Body (URB) | URB member list, committee descriptions, and leadership roles                            | documents/ABOUT_URB_GMU                              |
| 3   | GMU Elections and Disputes Commission (EDC) | EDC structure, authority, member list, and two internal agencies                         | documents/ABOUT_UDC_GMU                              |
| 4   | GMU URB Agencies                            | Student Culinary Council and Student Parking Board descriptions and members              | documents/URB_AGENCIES                               |
| 5   | GMU RSO FAQ                                 | FAQ on finding, joining, and starting Registered Student Organizations at Mason          | documents/FAQ_RSO_GMU                                |
| 6   | GMU RSO Support & Resources                 | Benefits, resources, annual events, Imagination Station, voice walls for RSOs            | documents/RSO_Support_and_resources                  |
| 7   | GMU Student Groups Directory                | CSV listing 500+ student organizations with categories and membership durations          | documents/gmu_groups.csv                             |
| 8   | GMU Guide: Start an Organization            | Step-by-step guide to starting a new RSO at George Mason University                      | documents/Guide_to_start_an_organization_gmu         |
| 9   | 6 Ways Students Can Demonstrate Leadership  | Article on leadership behaviors students can practice on campus                          | documents/6_ways_students_can_demonstrate_leadership |
| 10  | How to Become a Student Leader on Campus    | General guide on student leadership qualities, opportunities, and emotional intelligence | documents/How_to_become_a_student_leader             |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 500 characters

**Overlap:** 50 characters

**Reasoning:** Most of my documents are fairly short and self-contained — things like FAQ entries, committee descriptions, and bullet-pointed leadership tips. 500 characters felt like a sweet spot: big enough to hold a complete thought (like a full FAQ answer or a committee description), but small enough that I'm not stuffing unrelated content into the same chunk. The 50-character overlap is mostly there as a safety net for cases where a sentence gets cut right at a boundary to avoid losing the tail end of something important. The CSV of student organizations is the one exception; rows there are short and structured, so chunking by row or small row groups makes more sense than strict character splits.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** all-MiniLM-L6-v2 is a solid option here, since it's fast, runs locally, and doesn't need an API key. But if this were a real tool that students actually used, I'd think harder about the tradeoffs. The main one is domain specificity: MiniLM was trained on general text, and some of the GMU-specific terminology (committee names, org categories, acronyms like "URB" or "EDC") might not embed as meaningfully as it would with a model fine-tuned on university or government text. I'd also consider text-embedding-3-small from OpenAI if latency and cost were acceptable — it has a much larger context window and generally better semantic accuracy. Multilingual support isn't a big concern here since all documents are in English, but if this were expanded to serve Mason's student population in our korea campus, that would become a real factor.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| #   | Question                                                                                           | Expected answer                                                                                                                                                                              |
| --- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | How many seats are in the Undergraduate Representative Body, and how are they distributed?         | 50 total seats — 20 academic college seats (2 per college) and 30 at-large seats                                                                                                             |
| 2   | What is the RSO HUB and what can you use it for?                                                   | It's a one-stop resource for club officers to start a club, apply for funding, re-register an existing club, and explore officer roles                                                       |
| 3   | What committees can a URB representative sit on?                                                   | Administrative and Financial Affairs, University Academics, Diversity Equity and Inclusion, Government and Community Relations, University Services, and Student Engagement and Support      |
| 4   | What are two concrete ways a student can demonstrate leadership without holding an official title? | practicing empathy (letting others speak first, attending cultural events), taking accountability for mistakes, or assuming positive intent in conflicts                                     |
| 5   | What resources does an RSO get access to after registering with Student Involvement?               | Guidance from the RSO Support Team, eligibility for Student Funding Board funding, access to campus space at discounted or no cost, Mason360 presence, and access to the Imagination Station |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The CSV is structured data. The gmu_groups.csv file lists 500+ organizations in a table format, which doesn't chunk well with a plain character splitter. If I just run it through the same chunking logic as everything else, I'll end up with chunks that cut through row boundaries and produce garbled, half-row text. I'll need to handle it separately: either chunk by row, or convert each row into a short sentence like "The Artificial Intelligence Club is a Registered Student Organization in the Academic, STEM, and Computer/Technology categories.

2. Short documents might retrieve poorly against broad queries. Several of my documents (like URB_AGENCIES or ABOUT_UDC_GMU) are quite short. If a user asks something general like "how do I get involved in student government?", the retriever might surface chunks from the general leadership articles instead of the GMU-specific governance pages, just because the semantic overlap with those broader documents is higher. I might need to tune top-k or add some metadata filtering to prefer GMU-specific sources for GMU-specific questions.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

┌─────────────────────────────────────────────────────────────────────┐
│ RAG Pipeline │
└─────────────────────────────────────────────────────────────────────┘

[1] Document Ingestion - Plain text files: read directly with open() - CSV: pandas, convert rows to sentence strings
│
▼
[2] Chunking - Library: custom chunk_text() using character splits - Chunk size: 500 chars, overlap: 50 chars - CSV handled separately (row-level chunking)
│
▼
[3] Embedding + Vector Store - Embedding model: all-MiniLM-L6-v2 (sentence-transformers) - Vector store: ChromaDB (local, persistent)
│
▼
[4] Retrieval - Query embedded with same model - Top-5 chunks retrieved by cosine similarity from Chroma
│
▼
[5] Generation - Retrieved chunks formatted into a context block - Sent to OpenAI GPT-4o-mini with a grounding system prompt - Response returned via a simple CLI or Gradio interface

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:** I'll give claude the Documents table from this file plus the Chunking Strategy section and ask it to implement an ingest.py script with a load_documents() function and a chunk_text() function matching my 500/50 spec. I'll also tell it about the CSV edge case and ask it to handle that separately by converting rows to sentence strings. I'll verify the output by checking that chunks from a known document are the right length and don't cut mid-sentence too aggressively.

**Milestone 4 — Embedding and retrieval:** I'll give claude the Architecture diagram and the Retrieval Approach section and ask it to implement embed_and_store.py using sentence-transformers and ChromaDB. I'll ask it to produce a retrieve(query, k=5) function that returns the top-5 chunks with their source filenames. I'll test it manually with one of my evaluation questions (like the URB seat question) and check that the relevant chunks from ABOUT_URB_GMU actually come back in the top 5.

**Milestone 5 — Generation and interface:** I'll give claude my grounding instruction, the retrieval output format from Milestone 4, and ask it to implement a generate.py and app.py (streamlit) that builds a context block from retrieved chunks and calls groq with a strict system prompt. I'll run all 5 evaluation questions through it and compare outputs to my expected answers table above to judge accuracy.
