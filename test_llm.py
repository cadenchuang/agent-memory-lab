
from llm_answer import answer_with_llm

memories = [
    {
        "source": "user",
        "key": "meeting_day",
        "value": "Thursday"
    },
    {
        "source": "document",
        "key": "meeting_day",
        "value": "Friday"
    }
]

result = answer_with_llm(
    memories,
    "What day is my meeting?"
)

print("Model answer:", result)
