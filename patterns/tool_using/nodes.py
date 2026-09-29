from config.llm import get_llm
from tools.calculator import calculator
from .state import AgentState

llm = get_llm()


def reasoning_agent(state: AgentState) -> dict:
    """
    Classifies the user's question as MATH or GENERAL.
    If MATH, converts the question into a Python math expression.
    If GENERAL, sets category so the router sends it to the fallback agent.
    """
    prompt = f"""You are a smart classification and reasoning agent.

First, determine if the following question is a MATH question (requires arithmetic
calculation) or a GENERAL knowledge question.

If it is a MATH question:
  - Respond with exactly two lines:
    Line 1: MATH
    Line 2: A valid Python math expression that answers the question.

If it is a GENERAL question:
  - Respond with exactly one line:
    GENERAL

Examples:

Question: What is the sum of 5 and 3?
MATH
5 + 3

Question: What is the average of 100 and 200?
MATH
(100 + 200) / 2

Question: Define AI
GENERAL

Question: Who is the president of the United States?
GENERAL

Question: What is the square of the average of 100 and 200?
MATH
((100 + 200) / 2) ** 2

Question: {state['question']}
"""
    response = llm.invoke(prompt).content.strip()
    lines = response.split("\n")

    category = lines[0].strip().upper()

    if category == "MATH" and len(lines) >= 2:
        expression = lines[1].strip()
        return {"category": "MATH", "expression": expression}
    else:
        return {"category": "GENERAL", "expression": ""}


def tool_executor(state: AgentState) -> dict:
    """Executes the calculator tool on the extracted math expression."""
    result = calculator(state["expression"])
    return {"result": result}


def general_agent(state: AgentState) -> dict:
    """Fallback agent that answers general (non-math) questions using the LLM."""
    prompt = f"""You are a helpful, knowledgeable AI assistant.
Answer the following question clearly and concisely.

Question: {state['question']}
"""
    response = llm.invoke(prompt).content.strip()
    return {"result": response}