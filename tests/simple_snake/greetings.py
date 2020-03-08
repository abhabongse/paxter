name = "John Smith"
age = 47
occupation = "Student"


def strip(text: str) -> str:
    return text.strip()


def tag(text: str, label: str) -> str:
    return f"<{label}>{text}</{label}>"
