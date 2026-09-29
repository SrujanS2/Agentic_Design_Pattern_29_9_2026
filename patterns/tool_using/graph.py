from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import reasoning_agent, tool_executor, general_agent


def route_question(state: AgentState) -> str:
    """Routes to math_agent or general_agent based on the classification."""
    if state.get("category") == "MATH":
        return "math_agent"
    return "general_agent"


def build_graph():
    graph = StateGraph(AgentState)

    # --- Nodes ---
    graph.add_node("reasoning_agent", reasoning_agent)
    graph.add_node("math_agent", tool_executor)
    graph.add_node("general_agent", general_agent)

    # --- Edges ---
    graph.set_entry_point("reasoning_agent")

    # Conditional routing after classification
    graph.add_conditional_edges(
        "reasoning_agent",
        route_question,
        {
            "math_agent": "math_agent",
            "general_agent": "general_agent",
        },
    )

    graph.add_edge("math_agent", END)
    graph.add_edge("general_agent", END)

    return graph.compile()