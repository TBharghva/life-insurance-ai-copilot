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