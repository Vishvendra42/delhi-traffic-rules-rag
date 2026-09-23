import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from src.retriever import Retriever

load_dotenv()


class Generator:

    def __init__(self):
        self.retriever = Retriever()

        self.llm = ChatGroq(
            model_name="openai/gpt-oss-20b",
            temperature=0.3,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def generate(self, query, top_k=5):

        # Step 1: Retrieve relevant chunks
        results = self.retriever.search(query, top_k)

        # Step 2: Combine retrieved chunks
        context = "\n\n".join(
            result["text"] for result in results
        )

        # Step 3: Instructions for the LLM
        system_message = SystemMessage(
            content="""
You are a Delhi Traffic Rules Assistant.

Your job is to answer questions about Delhi traffic rules,
penalties, driving licences, vehicle registration, documents,
road safety, speed limits and challans.

Rules:

1. Use only the retrieved knowledge provided to answer the question.
2. Do not invent fines, rules, section numbers, fees or procedures.
3. If the retrieved knowledge does not contain enough information,
   clearly say that the information is not available.
4. Give the direct answer first.
5. Mention the relevant Act, Section, Rule or source when available.
6. Clearly distinguish between fines, imprisonment, court penalties,
   and licence suspension or disqualification.
7. Use Delhi-specific information only.
8. Ignore retrieved information that is unrelated to the question.
9. If different penalties are given for first and subsequent offences,
   clearly mention the difference.
10. Keep the answer clear, factual and concise.

If the answer cannot be established from the retrieved knowledge,
say:

"I could not find sufficient information about this in the
Delhi Traffic Rules knowledge base."
"""
        )

        # Step 4: Create the user message
        user_message = HumanMessage(
            content=f"""
Use the following retrieved Delhi Traffic Rules knowledge to answer
the user's question.

--- RETRIEVED KNOWLEDGE ---
{context}
--- END KNOWLEDGE ---

USER QUESTION:
{query}

Answer the question directly. Do not use information that is not
supported by the retrieved knowledge.
"""
        )

        # Step 5: Ask the LLM
        response = self.llm.invoke([
            system_message,
            user_message
        ])

        # Step 6: Return the answer
        return response.content


if __name__ == "__main__":

    generator = Generator()

    question = "What is the fine for driving without a licence?"

    answer = generator.generate(question)

    print("\nAnswer:")
    print(answer)