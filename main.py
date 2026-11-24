
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not api_key:
    raise ValueError("OpenAI API key not found in .env")

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are NEXUS AI, an intelligent digital employee.

Your responsibilities:
1. Understand employee instructions.
2. Analyze the requested work.
3. Break complex tasks into logical steps.
4. Explain your execution plan.
5. Identify risks and required approvals.
6. Never claim a task was completed unless it was actually completed.

You are professional, accurate and proactive.

You must distinguish between planning a task and executing it.
"""


def ask_nexus(employee_instruction):

    response = client.responses.create(
        model=model,
        instructions=SYSTEM_PROMPT,
        input=employee_instruction
    )

    return response.output_text


if __name__ == "__main__":

    print("\n========== NEXUS AI ==========")
    print("Your Intelligent Digital Employee")
    print("==============================\n")

    instruction = input("Employee: ")

    print("\nNEXUS is thinking...\n")

    try:
        result = ask_nexus(instruction)
        print("NEXUS AI:\n")
        print(result)

    except Exception as error:
        print("Error:", error)
