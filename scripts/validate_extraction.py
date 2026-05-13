from pathlib import Path

markdown_files = Path(
    "datasets/processed/markdown"
).glob("*.md")

for file in markdown_files:

    content = file.read_text(encoding="utf-8")

    print(f"\nChecking: {file.name}")

    # Basic validation
    print(f"Characters: {len(content)}")

    heading_count = content.count("#")

    print(f"Headings found: {heading_count}")

    table_count = content.count("|")

    print(f"Table markers found: {table_count}")