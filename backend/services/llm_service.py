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