"""Build one Markdown file that contains the whole Task 2 program.

Run this script from the 'task 2' folder:
    python3 build_code_markdown.py
"""

import os

PROGRAM_FOLDER = "program"
OUTPUT_FILE = "Adam Heier - Task 2 - Code.md"

SECTIONS = [
    ("Main program", "main.py", "python"),
    ("Program logic (all classes)", "fraud_detection.py", "python"),
    ("Test program", "test.py", "python"),
    ("Transaction data", "transactions.txt", "text"),
    ("Customer account data", "accounts.csv", "text"),
    ("Rule configuration", "rules_config.json", "json"),
]


def read_file(name):
    """Return the content of a file inside the program folder."""
    path = os.path.join(PROGRAM_FOLDER, name)
    with open(path, "r", encoding="utf-8") as source_file:
        return source_file.read().rstrip("\n")


def main():
    """Write all program files into one Markdown document."""
    parts = [
        "# Adam Heier - ICT703 Task 2 - Python Program\n",
        "Bank Transaction Fraud Detection System. These six files are "
        "the complete submission (`Adam Heier - Task 2.zip`).\n",
        "Run with `python main.py`, test with `python test.py` from the "
        "program folder. The `output/` folder with the CSV results is "
        "created by the program itself.\n",
        "## Contents\n",
    ]
    for title, name, _ in SECTIONS:
        parts.append(f"- [`{name}`](#{name.replace('.', '')}) - {title}")
    parts.append("")
    for title, name, language in SECTIONS:
        parts.append(f"## `{name}`\n")
        parts.append(f"*{title}*\n")
        parts.append(f"```{language}")
        parts.append(read_file(name))
        parts.append("```\n")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as markdown_file:
        markdown_file.write("\n".join(parts))
    print(f"{OUTPUT_FILE} written ({os.path.getsize(OUTPUT_FILE)} bytes)")


if __name__ == "__main__":
    main()
