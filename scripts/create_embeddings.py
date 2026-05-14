import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

import os


# ---------------------------------------------------
# INPUT FILES
# ---------------------------------------------------

TEXT_CHUNKS_PATH = Path(
    "datasets/chunks/text_chunks.json"
)

TABLE_CHUNKS_PATH = Path(
    "datasets/chunks/table_chunks.json"
)


# ---------------------------------------------------
# OUTPUT DIRECTORIES
# ---------------------------------------------------

TEXT_INDEX_DIR = Path(
    "vectorstores/text_index"
)

TABLE_INDEX_DIR = Path(
    "vectorstores/table_index"
)

TEXT_INDEX_DIR.mkdir(parents=True, exist_ok=True)

TABLE_INDEX_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------
# LOAD CHUNKS
# ---------------------------------------------------

print("\nLoading chunk files...")

with open(TEXT_CHUNKS_PATH, "r", encoding="utf-8") as f:
    text_chunks = json.load(f)

with open(TABLE_CHUNKS_PATH, "r", encoding="utf-8") as f:
    table_chunks = json.load(f)

print(f"Loaded text chunks: {len(text_chunks)}")

print(f"Loaded table chunks: {len(table_chunks)}")


# ---------------------------------------------------
# CONVERT TO LANGCHAIN DOCUMENTS
# ---------------------------------------------------

text_documents = []

table_documents = []


# Convert text chunks
for chunk in text_chunks:

    document = Document(
        page_content=chunk["text"],
        metadata=chunk["metadata"]
    )

    text_documents.append(document)


# Convert table chunks
for chunk in table_chunks:

    document = Document(
        page_content=chunk["text"],
        metadata=chunk["metadata"]
    )

    table_documents.append(document)


print(f"\nPrepared text documents: {len(text_documents)}")

print(f"Prepared table documents: {len(table_documents)}")


# ---------------------------------------------------
# INITIALIZE EMBEDDING MODEL
# ---------------------------------------------------

print("\nInitializing embedding model...")


# Uses OpenAI API key from environment variables
#
# Required:
# set OPENAI_API_KEY=your_key
#
# Recommended model:
# text-embedding-3-small
#
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv('OPENAI_API_KEY')
)


# ---------------------------------------------------
# CREATE TEXT VECTOR STORE
# ---------------------------------------------------

print("\nCreating text FAISS index...")


text_vectorstore = FAISS.from_documents(
    documents=text_documents,
    embedding=embeddings
)


# Save locally
text_vectorstore.save_local(
    str(TEXT_INDEX_DIR)
)

print(
    f"Saved text vector index to: "
    f"{TEXT_INDEX_DIR}"
)


# ---------------------------------------------------
# CREATE TABLE VECTOR STORE
# ---------------------------------------------------

print("\nCreating table FAISS index...")


table_vectorstore = FAISS.from_documents(
    documents=table_documents,
    embedding=embeddings
)


# Save locally
table_vectorstore.save_local(
    str(TABLE_INDEX_DIR)
)

print(
    f"Saved table vector index to: "
    f"{TABLE_INDEX_DIR}"
)


# ---------------------------------------------------
# SUMMARY
# ---------------------------------------------------

print("\nEmbedding pipeline completed successfully.")

print(
    f"Total embedded text chunks: "
    f"{len(text_documents)}"
)

print(
    f"Total embedded table chunks: "
    f"{len(table_documents)}"
)