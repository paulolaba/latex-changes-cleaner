# LaTeX Changes Cleaner

A Python script to process LaTeX documents that use the [`changes`](https://ctan.org/pkg/changes) package.  
It generates a **clean version** of your `.tex` file by removing or transforming markup commands, leaving only the final version of the text (ready for submission).

---

## Features

Reads a `.tex` file and processes the following commands:

- `\added[id=XYZ]{...}` or `\added{...}`  
  → keeps only the content inside the braces  

- `\deleted[id=XYZ]{...}` or `\deleted{...}`  
  → removes the entire command and its content  

- `\replaced[id=XYZ]{new}{old}` or `\replaced{new}{old}`  
  → keeps only the `new` content  

The script handles **balanced braces** and avoids common issues with line breaks in LaTeX.

---

## Usage

Run the script directly from the terminal:

```bash
python3 clean_changes.py your_file.tex
