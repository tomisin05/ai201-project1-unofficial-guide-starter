# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This system covers student leadership and involvement at George Mason University. Specifically, it answers questions about how to get involved in student government (the URB, EDC, and Student Government), how to start or join a Registered Student Organization, what resources are available to student organizations, and general guidance on how to develop leadership skills as a student.

This knowledge is valuable because a lot of it is scattered across multiple GMU web pages, PDFs, and CSV exports that a prospective student leader would have to track down individually. The official GMU website tells you what committees exist, but doesn't give you a single place to ask "how do I actually get involved?" or "what can the RSO HUB do for me?" This system consolidates that into one searchable interface.

---

## Document Sources

| #   | Source                                                 | Type       | URL or file path                                       |
| --- | ------------------------------------------------------ | ---------- | ------------------------------------------------------ |
| 1   | GMU Student Government (About SG)                      | Plain text | `documents/ABOUT_SG_GMU`                               |
| 2   | GMU Undergraduate Representative Body                  | Plain text | `documents/ABOUT_URB_GMU`                              |
| 3   | GMU Elections and Disputes Commission                  | Plain text | `documents/ABOUT_UDC_GMU`                              |
| 4   | GMU URB Agencies (Culinary Council, Parking Board)     | Plain text | `documents/URB_AGENCIES`                               |
| 5   | GMU RSO Frequently Asked Questions                     | Plain text | `documents/FAQ_RSO_GMU`                                |
| 6   | GMU RSO Support and Resources                          | Plain text | `documents/RSO_Support_and_resources`                  |
| 7   | GMU Student Organizations Directory                    | CSV        | `documents/gmu_groups.csv`                             |
| 8   | GMU Guide: How to Start a Student Organization         | Plain text | `documents/Guide_to_start_an_organization_gmu`         |
| 9   | CU Boulder: 6 Ways Students Can Demonstrate Leadership | Plain text | `documents/6_ways_students_can_demonstrate_leadership` |
| 10  | How to Become a Student Leader on Campus               | Plain text | `documents/How_to_become_a_student_leader`             |

---

## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** Most documents in this corpus are short and structured — FAQ entries, committee descriptions, bulleted lists of leadership tips. They're not long research papers, so I don't need large chunks to preserve context. 500 characters is enough to hold a complete thought (a full FAQ answer, a committee description, a paragraph of advice) without pulling in unrelated content from the same document. The 50-character overlap is a small safety net to avoid losing the tail end of a sentence at a chunk boundary. The CSV of student organizations is the one exception: each row is converted into a readable sentence before chunking, so the chunker is working on prose rather than raw CSV data.

**Final chunk count:** 327 chunks across 10 documents

---

## Sample Chunks

These are five representative chunks drawn from the corpus, each labeled with its source document.

**Chunk 1** | source: `ABOUT_SG_GMU`

```
ment has undergone many changes throughout its history, but our mission and goal have remained focused on advocating for the students.

Student Government Leadership
The leadership of Student Government includes two elected positions:

The Undergraduate Student Body President
The Executive Vice President
Appointed leadership positions include:

the Vice President of Outreach
the Vice President of PR and Marketing
the Vice President for Membership Development and Training
Officers nominated and a
```

**Chunk 2** | source: `FAQ_RSO_GMU`

```
FAQs How do I find organizations to join? You can explore over 500 student-led groups by using Mason360. This platform allows you to browse through various categories, including Registered Student Organizations (RSOs), Club Sports, Fraternity & Sorority Life, and Campus-Wide Organizations.
```

**Chunk 3** | source: `RSO_Support_and_resources`

```
ficially recognized Mason student organization you will have access to the following benefits and perks:

RSO Support Team Guidance from the RSO Support Team

The RSO Support Team is here to help with every step!

Eligibility for Funding from Student Funding Board

Apply when your group needs funding assistance for events and other expenses.

Access to Campus Space at Discounted or No Cost
```

**Chunk 4** | source: `6_ways_students_can_demonstrate_leadership`

```
ir daily practice of demonstrating leadership can help students succeed in future opportunities.

Students can experience personal growth, skill development, enhanced relationships and an overall improved college experience. These practices and characteristics can help them shine as they seek official leadership positions during college, search for jobs and internships, and move into life after college.
```

**Chunk 5** | source: `gmu_groups.csv`

```
Girls Who Code at George Mason University is a Registered Student Organizations in the following categories: Academic, STEM, Special Interest, Computer/Technology. Membership lasts: Lifetime.
Girls Who Study is a Registered Student Organizations in the following categories: Academic. Membership lasts: Lifetime.
Global Action In Nursing is a Registered Student Organizations in the following categories: International/Multicultural, STEM, Volunteer/Service, Special Interest, Health/Wellness. Membership lasts: Lifetime.
```

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Production tradeoff reflection:** For this project, `all-MiniLM-L6-v2` is a solid option here, since it's fast, runs locally, doesn't need an API key, and handles general English text well. But if this were a real tool deployed to GMU students, I'd weigh a few tradeoffs.
Domain specificity: MiniLM was trained on general web text, so GMU-specific acronyms like "URB," "EDC," and "Mason360" may not embed as meaningfully as they would in a model fine-tuned on university or government text, this likely contributed to the weak retrieval on the RSO HUB query.
Context length: MiniLM has a 256-token limit, which means longer chunks get silently truncated at embedding time; a model like `text-embedding-3-small` from OpenAI supports 8,191 tokens and would handle longer documents much better.
Latency vs. accuracy: a locally-hosted model has zero API latency, but a hosted model like OpenAI's embeddings would likely produce more accurate similarity rankings at the cost of an API call per query.
For a production deployment, I'd probably use `text-embedding-3-small` or a fine-tuned BERT variant if the corpus is large enough to justify it.

---

## Grounded Generation

**System prompt grounding instruction:**

```
You are a helpful assistant for students at George Mason University who want to learn about
student leadership, student organizations, and student government.

Answer the user's question using ONLY the information provided in the context below. Do not
use any outside knowledge or information from your training data. Every claim in your answer
must be traceable to the provided context.

If the context does not contain enough information to answer the question, respond with
exactly: "I don't have enough information in my documents to answer that."

Be specific and direct. Do not pad your answer with generic advice.
```

The model temperature is set to 0.2 to reduce creative extrapolation and keep the model closer to the retrieved text.

**How source attribution is surfaced in the response:** Source attribution is handled programmatically in `generate.py`. After generation, the code collects the source filenames from the retrieved chunks and appends them to the response object. The Gradio interface then displays them in a separate "Retrieved from" panel. This guarantees attribution is always present regardless of whether the model chose to mention sources in its answer.

---

## Retrieval Test Results

**Query 1:** How many seats are in the Undergraduate Representative Body and how are they distributed?

| Rank | Source          | Distance | Why it's relevant                                                                                                                                 |
| ---- | --------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | `ABOUT_SG_GMU`  | 0.35     | Contains the exact sentence "There are 50 total seats, including 20 academic college seats (2 per college) and 30 at-large seats." — a direct hit |
| 2    | `ABOUT_URB_GMU` | 0.62     | Describes the URB's role and committee structure, providing supporting context                                                                    |
| 3    | `ABOUT_SG_GMU`  | 0.79     | Contains election timing information — adjacent topic, weaker match                                                                               |

The large gap between result 1 (0.35) and result 2 (0.62) shows the retriever found one clearly dominant chunk. This is a case where retrieval worked exactly as expected.

---

**Query 2:** What is the RSO HUB and what can you use it for?

| Rank | Source                      | Distance | Why it's relevant                                                                                                        |
| ---- | --------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------ |
| 1    | `FAQ_RSO_GMU`               | 1.06     | Mentions the RSO HUB at the end of a chunk, but the chunk ends mid-answer                                                |
| 2    | `RSO_Support_and_resources` | 1.13     | Covers RSO benefits but not the HUB definition specifically                                                              |
| 4    | `FAQ_RSO_GMU`               | 1.22     | Contains the actual HUB definition — but it starts mid-sentence because the definition was split across a chunk boundary |

All distances are above 1.0, which is notably weaker than Query 1. The RSO HUB definition appears in the FAQ document, but the chunker split the FAQ answer at a character boundary that fell in the middle of the definition. Result [4] has the most relevant text but starts with "ch Key Words..." — the beginning of the answer is in the previous chunk. This is a retrieval failure caused by the chunking stage.

---

**Query 3:** What resources does an RSO get after registering with Student Involvement?

| Rank | Source                               | Distance | Why it's relevant                                                         |
| ---- | ------------------------------------ | -------- | ------------------------------------------------------------------------- |
| 1    | `RSO_Support_and_resources`          | 0.71     | Directly lists the benefits and perks of registering — on target          |
| 2    | `Guide_to_start_an_organization_gmu` | 0.83     | Related to RSO registration process, supporting context                   |
| 4    | `FAQ_RSO_GMU`                        | 0.84     | Describes RSO definition and Mason360 — adjacent but not the exact answer |

Result 1 is clearly the right chunk. Results 2–5 are loosely related but acceptable — the LLM used result 1 as the primary source and produced an accurate answer.

---

## Example Responses

**Response 1 — Grounded, with sources:**

> Q: What resources does an RSO get access to after registering with Student Involvement?
>
> A: After registering with Student Involvement, an RSO gets access to the following benefits and perks:
>
> 1. Guidance from the RSO Support Team
> 2. Eligibility for Funding from Student Funding Board
> 3. Access to Campus Space at Discounted or No Cost through the campus space/room reservation system, 25Live
>
> Additionally, RSOs can take advantage of community opportunities and stay up-to-date with information through Mason360 News and Newsletters. They also have access to annual opportunities such as the Fall Get Connected Fair and GAMEmason.
>
> **Retrieved from:** RSO_Support_and_resources, FAQ_RSO_GMU, ABOUT_URB_GMU, Guide_to_start_an_organization_gmu

---

**Response 2 — Grounded, with sources:**

> Q: How many seats are in the Undergraduate Representative Body and how are they distributed?
>
> A: There are 50 total seats in the Undergraduate Representative Body. The seats are distributed as follows: 20 academic college seats (2 per college) and 30 at-large seats.
>
> **Retrieved from:** ABOUT_SG_GMU, ABOUT_URB_GMU

---

**Response 3 — Out-of-scope refusal:**

> Q: What is the best pizza place near campus?
>
> A: I don't have enough information in my documents to answer that.
>
> **Retrieved from:** URB_AGENCIES, How_to_become_a_student_leader, ABOUT_SG_GMU

The system correctly declined to answer rather than generating a plausible-sounding recommendation from training data.

---

## Query Interface

The interface is built with Gradio and runs at `http://localhost:7860` via `python app.py`.

**Input fields:**

- A text box labeled "Your question" — accepts any free-text question about GMU student leadership or organizations. Pressing Enter or clicking "Ask" submits the query.

**Output fields:**

- "Answer" — the grounded response generated by the LLM, based only on retrieved documents
- "Retrieved from" — a list of source document filenames that were used to construct the answer

Five example questions are pre-loaded as clickable buttons below the input box.

**Sample interaction transcript:**

```
User: What committees can a URB representative sit on?

Answer: According to the context, a URB representative is required to sit on two committees
per semester. The committees available are:

1. Administrative and Financial Affairs
2. University Academics
3. Diversity Equity and Inclusion
4. Government and Community Relations
5. University Services
6. Student Engagement and Support

Retrieved from:
• ABOUT_URB_GMU
• ABOUT_SG_GMU
• ABOUT_UDC_GMU
```

---

## Evaluation Report

| #   | Question                                                                                           | Expected answer                                                                                                                                                 | System response (summarized)                                                                                                           | Retrieval quality  | Response accuracy  |
| --- | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------ |
| 1   | How many seats are in the URB and how are they distributed?                                        | 50 total — 20 academic college seats (2 per college) and 30 at-large                                                                                            | "There are 50 total seats... 20 academic college seats (2 per college) and 30 at-large seats."                                         | Relevant           | Accurate           |
| 2   | What is the RSO HUB and what can you use it for?                                                   | One-stop resource for starting a club, applying for funding, re-registering, exploring officer roles                                                            | "A one-stop resource destination... to start a new club or manage an existing one." Missed: funding and re-registration details        | Partially relevant | Partially accurate |
| 3   | What committees can a URB representative sit on?                                                   | All 6: Administrative and Financial Affairs, University Academics, DEI, Government and Community Relations, University Services, Student Engagement and Support | Listed all 6 correctly, though briefly confused "University Academics" and "University Services" in the note                           | Relevant           | Partially accurate |
| 4   | What are two concrete ways a student can demonstrate leadership without holding an official title? | Examples from docs: practice empathy, take accountability, assume positive intent, promote excellence                                                           | Named two specific examples (showing up to intramural practice, doing readings for class discussions) — both traceable to the document | Relevant           | Accurate           |
| 5   | What resources does an RSO get access to after registering with Student Involvement?               | RSO Support Team, Student Funding Board eligibility, discounted campus space, Mason360 presence, Imagination Station                                            | Listed the top 3 benefits plus Mason360 and annual events — accurate and complete                                                      | Relevant           | Accurate           |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** What is the RSO HUB and what can you use it for?

**What the system returned:** "The RSO HUB is a one-stop resource destination designed to help club officers and members pursue their goals. You can use it to get help with starting a new club or managing an existing one." The answer is partially correct but omits key uses listed in the source document: applying for funding, re-registering an existing club, and exploring officer roles.

**Root cause (tied to a specific pipeline stage):** The failure originates in the chunking stage. The full RSO HUB definition in `FAQ_RSO_GMU` reads: "The RSO HUB is a one-stop resource destination designed to help club officers and members pursue their goals. It provides essential information on how to start a club, apply for funding, re-register an existing club, and explore officer roles." This sentence spans a chunk boundary — the first half landed at the tail of one chunk, and the second half ("It provides essential information on how to start a club...") landed at the start of the next. When retrieval ran, it returned the chunk containing only the first half of the definition (result [1], distance 1.06) and a later chunk that starts mid-sentence with "ch Key Words" (result [4], distance 1.22). The model only saw the incomplete first half and generated an incomplete answer.

All retrieval distances for this query were above 1.0, indicating the embedding model struggled to find a strong match. This is partly because the query "What is the RSO HUB" is a definitional question, and the most relevant chunk doesn't start with the definition — it starts with text from a different FAQ answer, which dilutes the semantic signal.

**What you would change to fix it:** Two changes would help. First, chunk on FAQ question boundaries rather than fixed character counts — split `FAQ_RSO_GMU` at each "Q:" header so each FAQ entry is its own chunk, guaranteeing the full answer stays together. Second, increase overlap from 50 to 100–150 characters so that a sentence straddling a boundary appears fully in at least one chunk.

---

## Spec Reflection

**One way the spec helped you during implementation:** The planning.md section on anticipated challenges pushed me to think about the CSV document before writing any code. I had listed "the CSV is structured data, not prose" as a known risk, which meant I went into `ingest.py` already knowing I needed a separate CSV handler. Instead of discovering mid-way through that `chunk_text()` was producing garbled half-rows, I wrote `load_csv_as_text()` upfront to convert each row into a readable sentence. That one pre-planned decision prevented a whole class of bad chunks from ever entering the vector store.

**One way your implementation diverged from the spec, and why:** The spec listed OpenAI's GPT-4o-mini as the generation model, but the starter repo was wired for Groq with a free Groq API key already in `.env.example`. Switching to Groq's `llama-3.3-70b-versatile` was the more practical choice — it required no credit card, had no rate-limit surprises, and was already scaffolded in `requirements.txt`. The quality difference for this domain turned out to be negligible; both models follow the grounding instruction reliably on short-context retrieval tasks like this one.

---

## AI Usage

**Instance 1**

- _What I gave the AI:_ The Documents table and Chunking Strategy section from `planning.md`, plus a description of the CSV edge case (structured data that doesn't chunk like prose).
- _What it produced:_ A complete `ingest.py` with `load_documents()`, `clean_text()`, and `chunk_text()` functions, plus a separate `load_csv_as_text()` that converted each CSV row into a sentence. The chunk size and overlap matched the spec exactly.
- _What I changed or overrode:_ The initial version used `pdfplumber` for the PDF document. After checking the actual file, I found the PDF had already been converted to plain text, so I removed the pdfplumber dependency and the PDF branch entirely, simplifying the loader.

**Instance 2**

- _What I gave the AI:_ The Retrieval Approach section and pipeline diagram from `planning.md`, asking it to implement `embed_and_store.py` using `sentence-transformers` and ChromaDB with source metadata, and a `retrieve()` function returning top-5 chunks with distances.
- _What it produced:_ Working `embed_and_store.py` and `retrieve.py` files that matched the spec. The retrieval function returned chunks with text, source, chunk index, and distance score.
- _What I changed or overrode:_ Pylance flagged three `reportOptionalSubscript` errors on the ChromaDB query result fields (`documents`, `metadatas`, `distances`), because ChromaDB's type stubs mark those as `Optional`. I added `or [[]]` guards on all three fields before subscripting to satisfy the type checker without changing the runtime behavior.
