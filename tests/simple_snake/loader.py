import os

import pytest

this_dir = os.path.dirname(os.path.abspath(__file__))


def load_test(prefix):
    env_file = os.path.join(this_dir, f"{prefix}.py")
    input_text_file = os.path.join(this_dir, f"{prefix}.in")
    expected_file = os.path.join(this_dir, f"{prefix}.expected")

    if not os.path.isfile(env_file):
        env_file = None

    return pytest.param(env_file, input_text_file, expected_file, id=prefix)


prefixes = [
    'delimiters', 'greetings', 'loading_functions', 'loops_and_conds', 'write_buffer',
]
all_test_cases = [load_test(prefix) for prefix in prefixes]
