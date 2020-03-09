name = "John"
age = 25
bold = lambda token: f"<b>{token}</b>"  # noqa: E731
italic = lambda token: f"<i>{token}</i>"  # noqa: E731
tag = lambda token, tag: f"<{tag}>{token}</{tag}>"  # noqa: E731
