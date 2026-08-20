

import re

MAX_INPUT_LENGTH = 500

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+the\s+previous\s+instructions",
    r"you\s+are\s+now",
    r"pretend\s+you\s+are",
    r"act\s+as\s+if\s+you\s+are",
    r"reveal\s+your\s+(system\s+)?prompt",
    r"reveal\s+your\s+system\s+instructions",
    r"system\s+prompt",
]

SENSITIVE_PATTERNS = [
    r"password\s*=",
    r"api[_-]?key\s*=",
    r"token\s*=",
    r"secret\s*=",
]


def validate_input(prompt):
    if len(prompt) > MAX_INPUT_LENGTH:
        return False, "Input exceeds 500 characters."

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return False, "Potential prompt injection detected."

    return True, ""


def scan_output(response):
    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            return False, "Potential sensitive information detected."

    if re.search(r"https?://", response, re.IGNORECASE):
        return False, "Unsolicited external URL detected."

    return True, ""