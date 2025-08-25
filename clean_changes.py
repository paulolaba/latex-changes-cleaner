#!/usr/bin/python3
import re
import sys
import os

"""
2025-05-14T21:29:13 (P. Laba)
- We'll use regex to clean up edits made with the LaTeX changes package.

2025-05-15T11:01:25 (P. Laba)
- In the new version, we'll combine regex and indices to solve the line break issue.
- You must run this script directly from the terminal with:
python3 clean_changes.py your_file.tex

2025-05-16T12:14:45 (P. Laba)
- Output filename logic updated: if input has '-changes', remove it for output; otherwise, append '-cleaned'.
"""

def find_balanced_braces(text, start_index):
    """
    Returns the full content enclosed in balanced braces starting from start_index.
    Also returns the index right after the closing brace.
    """
    if text[start_index] != '{':
        raise ValueError("Expected opening brace at the start index")

    depth = 0
    for i in range(start_index, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[start_index+1:i], i + 1

    raise ValueError("Unbalanced braces in LaTeX content")

def clean_changes_commands(input_tex, output_tex):
    r"""
    Reads a .tex file, removes or transforms commands from the 'changes' package:
    - \added[id=XYZ]{...} or \added{...}       → keep only the content inside the braces
    - \deleted[id=XYZ]{...} or \deleted{...}   → remove the entire command and its content
    - \replaced[id=XYZ]{new}{old} or \replaced{new}{old} → keep only the 'new' content

    Writes the cleaned content to a new .tex file.
    """
    with open(input_tex, 'r', encoding='iso-8859-1') as f:
        content = f.read()

    output = ""
    i = 0
    while i < len(content):
        match = re.match(r'\\(added|deleted|replaced)(\[[^\]]*?\])?', content[i:])
        if match:
            cmd = match.group(1)
            i += match.end()

            try:
                if cmd == 'added':
                    if content[i] != '{':
                        output += f"\\{cmd}"
                        continue
                    inner, next_i = find_balanced_braces(content, i)
                    output += inner
                    i = next_i

                elif cmd == 'deleted':
                    if content[i] != '{':
                        continue
                    _, next_i = find_balanced_braces(content, i)
                    i = next_i

                elif cmd == 'replaced':
                    if content[i] != '{':
                        continue
                    new_text, next_i = find_balanced_braces(content, i)
                    if content[next_i] != '{':
                        continue
                    _, final_i = find_balanced_braces(content, next_i)
                    output += new_text
                    i = final_i

            except ValueError:
                output += content[i]
                i += 1

        else:
            output += content[i]
            i += 1

    with open(output_tex, 'w', encoding='iso-8859-1') as f:
        f.write(output)

    print(f"Cleaned file saved as: {output_tex}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 clean-changes.py <input_file.tex>")
        sys.exit(1)

    input_file = sys.argv[1]
    base, ext = os.path.splitext(input_file)

    if "-changes" in base:
        output_base = base.replace("-changes", "")
    else:
        output_base = f"{base}-cleaned"

    output_file = f"{output_base}{ext}"

    clean_changes_commands(input_file, output_file)

