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
    model="text-embedding-3-small",
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