import re


def clean_llm_response(response: str) -> str:
    """
    Remove reasoning tags like <think>...</think>
    and return clean final answer.
    """
    if not response:
        return "No answer generated"

    # remove think blocks
    cleaned = re.sub(
        r"<think>.*?</think>",
        "",
        response,
        flags=re.DOTALL | re.IGNORECASE
    )

    # remove extra spaces/newlines
    cleaned = cleaned.strip()

    return cleaned if cleaned else "No answer generated"