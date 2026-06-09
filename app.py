"""
app.py — Gradio interface for the GMU Student Leadership RAG system.

Run with:  python app.py
Then open:  http://localhost:7860
"""

import gradio as gr
from generate import ask


def handle_query(question: str):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)

    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="GMU Student Leadership Guide") as demo:
    gr.Markdown("## GMU Unofficial Student Leadership Guide")
    gr.Markdown(
        "Ask anything about student organizations, student government, or how to get involved "
        "in leadership at George Mason University. Answers are grounded in collected GMU documents."
    )

    with gr.Row():
        inp = gr.Textbox(
            label="Your question",
            placeholder="e.g. How do I start a new student organization at Mason?",
            lines=2,
        )

    btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        answer = gr.Textbox(label="Answer", lines=10, interactive=False)
        sources = gr.Textbox(label="Retrieved from", lines=10, interactive=False)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

    gr.Examples(
        examples=[
            ["How many seats are in the Undergraduate Representative Body?"],
            ["What is the RSO HUB and what can I use it for?"],
            ["What committees can a URB representative sit on?"],
            ["What resources does an RSO get after registering with Student Involvement?"],
            ["How can a student demonstrate leadership without holding an official title?"],
        ],
        inputs=inp,
    )


if __name__ == "__main__":
    demo.launch()
