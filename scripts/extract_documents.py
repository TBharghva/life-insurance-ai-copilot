from pathlib import Path
import json

from docling.document_converter import DocumentConverter


# ---------------------------------------------------
# PATHS
# ---------------------------------------------------

RAW_PDF_DIR = Path("datasets/raw/pdf")

MARKDOWN_OUTPUT_DIR = Path(
    "datasets/processed/markdown"
)

TABLE_OUTPUT_DIR = Path(
    "datasets/processed/tables"
)

METADATA_OUTPUT_DIR = Path(
    "datasets/processed/metadata"
)


# Create directories if not exist
MARKDOWN_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TABLE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
METADATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------
# INITIALIZE DOCLING
# ---------------------------------------------------

converter = DocumentConverter()


# ---------------------------------------------------
# PROCESS EACH PDF
# ---------------------------------------------------

for pdf_file in RAW_PDF_DIR.glob("*.pdf"):

    print(f"\nProcessing: {pdf_file.name}")

    # Convert PDF
    result = converter.convert(str(pdf_file))

    document = result.document

    # ---------------------------------------------------
    # EXPORT FULL DOCUMENT AS MARKDOWN
    # ---------------------------------------------------

    markdown_content = document.export_to_markdown()

    markdown_output_file = (
        MARKDOWN_OUTPUT_DIR / f"{pdf_file.stem}.md"
    )

    with open(markdown_output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"Markdown saved: {markdown_output_file}")


    # ---------------------------------------------------
    # EXTRACT TABLES
    # ---------------------------------------------------

    table_metadata = []

    for table_index, table in enumerate(document.tables):

        # Export table as markdown
        table_markdown = table.export_to_markdown()

        table_file = (
            TABLE_OUTPUT_DIR /
            f"{pdf_file.stem}_table_{table_index + 1}.md"
        )

        with open(table_file, "w", encoding="utf-8") as f:
            f.write(table_markdown)

        print(f"Table saved: {table_file}")

        # Metadata for table
        table_metadata.append({
            "table_id": table_index + 1,
            "source_document": pdf_file.name,
            "table_file": str(table_file),
        })


    # ---------------------------------------------------
    # GENERATE DOCUMENT METADATA
    # ---------------------------------------------------

    metadata = {
        "source_document": pdf_file.name,
        "markdown_file": str(markdown_output_file),
        "tables": table_metadata
    }

    metadata_file = (
        METADATA_OUTPUT_DIR /
        f"{pdf_file.stem}_metadata.json"
    )

    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved: {metadata_file}")


print("\nExtraction completed.")