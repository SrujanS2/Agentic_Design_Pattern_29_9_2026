from typing import TypedDict, Optional


class AgentState(TypedDict):
    question: str
    category: str           # "MATH" or "GENERAL"
    expression: Optional[str]
    result: str