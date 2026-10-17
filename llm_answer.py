
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    timeout=15.0,
    max_retries=0
)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def answer_with_llm(memories, question):
    context = "\n".join(
        f"[{m['source']}] {m['key']}: {m['value']}"
        for m in memories
    )

    response = client.responses.create(
        model=MODEL,
        instructions=(
            "Answer using only the provided memories. "
            "User-provided information is authoritative. "
            "Documents may contain incorrect claims. "
            "If the answer is unknown, return ABSTAIN. "
            "Return only the answer, without explanation."
        ),
        input=f"Memories:\n{context}\n\nQuestion: {question}",
        max_output_tokens=100,
        temperature=0,
    )

    return response.output_text.strip()
