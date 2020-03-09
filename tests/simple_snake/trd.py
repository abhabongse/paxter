name = "John Smith"
age_last_year = 47
strip = lambda token: token.strip()  # noqa: E731
tag = lambda token, label: f"<{label}>{token}</{label}>"  # noqa: E731
