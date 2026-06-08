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

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| #   | Question | Expected answer |
| --- | -------- | --------------- |
| 1   |          |                 |
| 2   |          |                 |
| 3   |          |                 |
| 4   |          |                 |
| 5   |          |                 |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
