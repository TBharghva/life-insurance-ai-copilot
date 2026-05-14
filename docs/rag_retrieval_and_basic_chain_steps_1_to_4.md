# RAG Retrieval + Basic AI Chain (Steps 1–4)

This document implements:

1. Retrieval testing
2. Retrieval service
3. LLM service
4. Basic RAG chain

These steps transform your project from:

```text
static vector database
```

into:

```text
working AI insurance copilot
```

---

# STEP 1 — Retrieval Testing

Goal:

Validate that:
- FAISS indices load correctly
- embeddings work
- semantic retrieval quality is good
- metadata is preserved

---

# File

```text
scripts/test_retrieval.py
```

---

# Code

```python
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()


# ---------------------------------------------------
# LOAD EMBEDDING MODEL
# ---------------------------------------------------

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


# ---------------------------------------------------
# LOAD FAISS VECTOR STORE
# ---------------------------------------------------

vectorstore = FAISS.load_local(
    "vectorstores/text_index",
    embeddings,
    allow_dangerous_deserialization=True
)


# ---------------------------------------------------
# TEST QUERY
# ---------------------------------------------------

query = "What happens if policy lapses?"


# ---------------------------------------------------
# RETRIEVE DOCUMENTS
# ---------------------------------------------------

results = vectorstore.similarity_search(
    query=query,
    k=3
)


# ---------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------

print("\nQUERY:")
print(query)

print("\nRETRIEVED CHUNKS:\n")

for index, document in enumerate(results):

    print("=" * 80)

    print(f"RESULT {index + 1}")

    print("=" * 80)

    print("\nCONTENT:\n")
    print(document.page_content)

    print("\nMETADATA:\n")
    print(document.metadata)

    print("\n")
```

---

# How This Works

## FAISS.load_local()

Loads your previously generated vector index.

---

## similarity_search()

Converts:

```text
user query
```

into embeddings.

Then compares against:

```text
stored chunk embeddings
```

using vector similarity.

---

# GOOD Retrieval Example

Query:

```text
What happens if policy lapses?
```

Expected retrieval:
- lapse sections
- reinstatement sections
- grace period sections

---

# BAD Retrieval Example

Returns:
- glossary
- riders
- beneficiary rules

If retrieval is bad:
- revisit chunking
- revisit metadata
- revisit embedding strategy

---

# Run Script

```bash
python scripts/test_retrieval.py
```

---

# STEP 2 — Retrieval Service

Goal:

Centralize all retrieval logic.

This becomes reusable across:
- LangGraph nodes
- FastAPI endpoints
- evaluation scripts
- testing

---

# File

```text
app/services/retrieval_service.py
```

---

# Code

```python
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()


# ---------------------------------------------------
# EMBEDDING MODEL
# ---------------------------------------------------

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


# ---------------------------------------------------
# LOAD VECTOR STORES
# ---------------------------------------------------

text_vectorstore = FAISS.load_local(
    "vectorstores/text_index",
    embeddings,
    allow_dangerous_deserialization=True
)


table_vectorstore = FAISS.load_local(
    "vectorstores/table_index",
    embeddings,
    allow_dangerous_deserialization=True
)


# ---------------------------------------------------
# TEXT RETRIEVAL
# ---------------------------------------------------


def retrieve_text_chunks(query: str, k: int = 3):
    """
    Retrieve semantic text chunks.
    """

    return text_vectorstore.similarity_search(
        query=query,
        k=k
    )


# ---------------------------------------------------
# TABLE RETRIEVAL
# ---------------------------------------------------


def retrieve_table_chunks(query: str, k: int = 2):
    """
    Retrieve table chunks.
    """

    return table_vectorstore.similarity_search(
        query=query,
        k=k
    )


# ---------------------------------------------------
# COMBINED RETRIEVAL
# ---------------------------------------------------


def retrieve_context(query: str):
    """
    Retrieve both semantic text and tables.
    """

    text_results = retrieve_text_chunks(query)

    table_results = retrieve_table_chunks(query)

    return {
        "text_results": text_results,
        "table_results": table_results
    }
```

---

# Why This Service Matters

Without retrieval service:
- retrieval logic gets duplicated
- graph nodes become messy
- debugging becomes painful

This creates:

```text
single source of retrieval logic
```

---

# STEP 3 — LLM Service

Goal:

Centralize all LLM interaction.

This allows easy switching between:
- OpenAI
- Claude
- Gemini

without changing graph logic.

---

# File

```text
app/services/llm_service.py
```

---

# Install

```bash
pip install langchain-openai
```

---

# Code

```python
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI


# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()


# ---------------------------------------------------
# INITIALIZE MODEL
# ---------------------------------------------------

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.2
)


# ---------------------------------------------------
# GENERATE RESPONSE
# ---------------------------------------------------


def generate_response(prompt: str):
    """
    Generate LLM response.
    """

    response = llm.invoke(prompt)

    return response.content
```

---

# Why Temperature 0.2?

Insurance systems require:
- consistency
- lower hallucination
- deterministic answers

Lower temperature improves reliability.

---

# STEP 4 — Basic RAG Chain

Goal:

Connect:

```text
query
→ retrieval
→ prompt
→ LLM
→ final answer
```

This is your FIRST working AI assistant.

---

# File

```text
app/services/rag_service.py
```

---

# Code

```python
from app.services.retrieval_service import retrieve_context

from app.services.llm_service import generate_response


# ---------------------------------------------------
# FORMAT RETRIEVED DOCUMENTS
# ---------------------------------------------------


def format_documents(documents):
    """
    Convert retrieved docs into prompt context.
    """

    formatted_text = ""

    for document in documents:

        formatted_text += (
            f"\n\n"
            f"CONTENT:\n"
            f"{document.page_content}\n"
        )

    return formatted_text


# ---------------------------------------------------
# MAIN RAG FUNCTION
# ---------------------------------------------------


def generate_rag_response(user_query: str):
    """
    End-to-end RAG pipeline.
    """

    # ---------------------------------------------------
    # RETRIEVE CONTEXT
    # ---------------------------------------------------

    retrieval_results = retrieve_context(user_query)

    text_results = retrieval_results["text_results"]

    table_results = retrieval_results["table_results"]


    # ---------------------------------------------------
    # FORMAT CONTEXT
    # ---------------------------------------------------

    text_context = format_documents(text_results)

    table_context = format_documents(table_results)


    # ---------------------------------------------------
    # BUILD PROMPT
    # ---------------------------------------------------

    prompt = f"""
You are an AI insurance copilot.

Answer the user's question ONLY using the provided insurance context.

If the answer is not found in context, say:
'I could not find that information in the insurance documents.'

==============================
TEXT CONTEXT
==============================
{text_context}

==============================
TABLE CONTEXT
==============================
{table_context}

==============================
USER QUESTION
==============================
{user_query}

==============================
FINAL ANSWER
==============================
"""


    # ---------------------------------------------------
    # GENERATE RESPONSE
    # ---------------------------------------------------

    answer = generate_response(prompt)


    # ---------------------------------------------------
    # FORMAT CITATIONS
    # ---------------------------------------------------

    citations = []

    for document in text_results:

        citations.append(
            {
                "source_document": document.metadata.get(
                    "source_document"
                ),
                "section": document.metadata.get(
                    "section"
                )
            }
        )


    # ---------------------------------------------------
    # RETURN RESPONSE
    # ---------------------------------------------------

    return {
        "answer": answer,
        "citations": citations
    }
```

---

# Why This Is Important

This is your:

```text
FIRST COMPLETE AI SYSTEM
```

You now have:

```text
user query
 ↓
semantic retrieval
 ↓
context grounding
 ↓
LLM reasoning
 ↓
response generation
```

---

# Test RAG System

Create:

```text
scripts/test_rag.py
```

---

# Code

```python
from app.services.rag_service import generate_rag_response


query = "Can a minor be nominee?"

response = generate_rag_response(query)


print("\nANSWER:\n")
print(response["answer"])


print("\nCITATIONS:\n")

for citation in response["citations"]:
    print(citation)
```

---

# Run

```bash
python scripts/test_rag.py
```

---

# What You Should Validate

## GOOD SYSTEM

Question:

```text
What is grace period?
```

Answer:
- grounded in retrieved context
- references lapse/reinstatement sections
- no hallucination

---

## BAD SYSTEM

Answer:
- generic insurance knowledge
- fabricated numbers
- unrelated riders/policies

---

# Current Architecture Status

After these 4 steps your system becomes:

```text
Insurance Knowledge Base
    ↓
Semantic Retrieval Layer
    ↓
RAG Context Builder
    ↓
LLM Reasoning Layer
    ↓
AI Assistant
```

This is now ready for:
- FastAPI integration
- Streamlit integration
- LangGraph orchestration
- conversation memory
- underwriting workflows
- policy recommendation nodes

