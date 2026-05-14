from backend.services.retrieval_service import retrieve_context

from backend.services.llm_service import ( stream_response, generate_response )


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

def stream_rag_response(user_query: str):

    retrieval_results = retrieve_context(
        user_query
    )

    text_results = retrieval_results[
        "text_results"
    ]

    table_results = retrieval_results[
        "table_results"
    ]


    text_context = format_documents(
        text_results
    )

    table_context = format_documents(
        table_results
    )


    prompt = f"""
        You are an AI insurance copilot.

        Answer ONLY using provided context.

        TEXT CONTEXT:
        {text_context}

        TABLE CONTEXT:
        {table_context}

        USER QUESTION:
        {user_query}

        FINAL ANSWER:
    """


    citations = []

    for document in text_results:

        citations.append(
            {
                "source_document":
                    document.metadata.get(
                        "source_document"
                    ),

                "section":
                    document.metadata.get(
                        "section"
                    )
            }
        )


    return {
        "stream": stream_response(prompt),
        "citations": citations
    }