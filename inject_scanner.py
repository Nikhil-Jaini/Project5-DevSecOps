import sys

SYSTEM_PROMPT_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "system prompt",
    "reveal your instructions",
    "disregard previous instructions",
]

INJECTION_PHRASES = [
    "ignore previous",
    "ignore all previous",
    "forget previous instructions",
    "reveal the system prompt",
    "override the system instructions",
]


def scan_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().lower()

    findings = []

    for pattern in SYSTEM_PROMPT_PATTERNS:
        if pattern.lower() in content:
            findings.append(pattern)

    for phrase in INJECTION_PHRASES:
        if phrase.lower() in content:
            findings.append(phrase)

    return findings


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inject_scanner.py <file>")
        sys.exit(1)

    filename = sys.argv[1]
    findings = scan_file(filename)

    if findings:
        print("Prompt injection patterns detected:")
        for finding in findings:
            print(f"- {finding}")
        sys.exit(1)

    print("No prompt injection patterns detected.")