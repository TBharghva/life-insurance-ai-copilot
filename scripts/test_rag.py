import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.services.rag_service import generate_rag_response

from dotenv import load_dotenv


load_dotenv()


query = "What is grace period?"

response = generate_rag_response(query)


print("\nANSWER:\n")
print(response["answer"])


print("\nCITATIONS:\n")

for citation in response["citations"]:
    print(citation)