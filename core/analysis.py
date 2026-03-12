
def feedback_to_prompt(feedback_list: list[dict]) -> str:

    lines = []

    for i, entry in enumerate(feedback_list, start=1):

        source = entry["source"] or "unknown"
        context = entry["context"] or "unknown"
        text = entry["text"]

        line = f"{i}. {source} | {context} | {text}"

        lines.append(line)

    return "\n".join(lines)