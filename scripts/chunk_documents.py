import json
import re
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


# ---------------------------------------------------
# INPUT DIRECTORIES
# ---------------------------------------------------

MARKDOWN_DIR = Path("datasets/processed/markdown")

TABLE_DIR = Path("datasets/processed/tables")

METADATA_DIR = Path("datasets/processed/metadata")


# ---------------------------------------------------
# OUTPUT DIRECTORY
# ---------------------------------------------------

OUTPUT_DIR = Path("datasets/chunks")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------
# CHUNKING CONFIGURATION
# ---------------------------------------------------

# Moderate chunk size works well for insurance docs
TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=[
        "\n## ",
        "\n### ",
        "\n\n",
        "\n",
        ". ",
        " "
    ]
)


# ---------------------------------------------------
# STORAGE
# ---------------------------------------------------

text_chunks = []

table_chunks = []


# ---------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------


def extract_sections(markdown_text):
    """
    Split markdown into sections using headings.

    Returns list of:
    {
        section_title,
        content
    }
    """

    # Split on markdown headings
    pattern = r"(^## .*?$|^# .*?$)"

    matches = list(
        re.finditer(pattern, markdown_text, re.MULTILINE)
    )

    sections = []

    # No headings found
    if not matches:
        return [
            {
                "section_title": "Unknown",
                "content": markdown_text
            }
        ]

    for index, match in enumerate(matches):

        start = match.start()

        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(markdown_text)
        )

        section_text = markdown_text[start:end].strip()

        lines = section_text.splitlines()

        section_title = lines[0].replace("#", "").strip()

        content = "\n".join(lines[1:]).strip()

        sections.append(
            {
                "section_title": section_title,
                "content": content
            }
        )

    return sections


# ---------------------------------------------------
# PROCESS MARKDOWN FILES
# ---------------------------------------------------

for markdown_file in MARKDOWN_DIR.glob("*.md"):

    print(f"\nProcessing markdown: {markdown_file.name}")

    markdown_content = markdown_file.read_text(
        encoding="utf-8"
    )

    # Load metadata file if exists
    metadata_file = (
        METADATA_DIR /
        f"{markdown_file.stem}_metadata.json"
    )

    metadata = {}

    if metadata_file.exists():

        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    # ---------------------------------------------------
    # EXTRACT SEMANTIC SECTIONS
    # ---------------------------------------------------

    sections = extract_sections(markdown_content)

    # ---------------------------------------------------
    # PROCESS EACH SECTION
    # ---------------------------------------------------

    for section_index, section in enumerate(sections):

        section_title = section["section_title"]

        section_content = section["content"]

        # Skip empty sections
        if not section_content.strip():
            continue

        # ---------------------------------------------------
        # SPLIT LARGE SECTIONS
        # ---------------------------------------------------

        chunks = TEXT_SPLITTER.split_text(section_content)

        for chunk_index, chunk_text in enumerate(chunks):

            chunk_data = {
                "text": chunk_text,
                "metadata": {
                    "source_document": metadata.get(
                        "source_document",
                        markdown_file.name
                    ),
                    "section": section_title,
                    "chunk_type": "text",
                    "chunk_id": (
                        f"{markdown_file.stem}_"
                        f"section_{section_index + 1}_"
                        f"chunk_{chunk_index + 1}"
                    ),
                    "source_file": str(markdown_file)
                }
            }

            text_chunks.append(chunk_data)


# ---------------------------------------------------
# PROCESS TABLE FILES
# ---------------------------------------------------

for table_file in TABLE_DIR.glob("*.md"):

    print(f"Processing table: {table_file.name}")

    table_content = table_file.read_text(
        encoding="utf-8"
    )

    # Each table becomes one chunk
    table_chunk = {
        "text": table_content,
        "metadata": {
            "source_document": table_file.name,
            "chunk_type": "table",
            "chunk_id": table_file.stem,
            "source_file": str(table_file)
        }
    }

    table_chunks.append(table_chunk)


# ---------------------------------------------------
# SAVE OUTPUT FILES
# ---------------------------------------------------

text_chunk_output = OUTPUT_DIR / "text_chunks.json"

with open(text_chunk_output, "w", encoding="utf-8") as f:
    json.dump(text_chunks, f, indent=2)

print(f"\nSaved text chunks: {text_chunk_output}")


# Save table chunks

table_chunk_output = OUTPUT_DIR / "table_chunks.json"

with open(table_chunk_output, "w", encoding="utf-8") as f:
    json.dump(table_chunks, f, indent=2)

print(f"Saved table chunks: {table_chunk_output}")


# ---------------------------------------------------
# SUMMARY
# ---------------------------------------------------

print("\nChunking completed.")

print(f"Total text chunks: {len(text_chunks)}")

print(f"Total table chunks: {len(table_chunks)}")