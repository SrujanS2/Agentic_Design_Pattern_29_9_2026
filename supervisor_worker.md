# 👥 Agentic Design Pattern – Supervisor-Worker

Welcome to the world of Agentic AI! The **Supervisor-Worker** design pattern is one of the most practical and widely used patterns for building AI systems. 

Here is a simple, step-by-step breakdown of how this code works.

---

## 1. The High-Level Concept
Imagine you walk into a bank. You don't just walk up to a random desk; you first talk to the **Receptionist (Supervisor)**. You tell them what you need, and they direct you to the right person—either the **Loan Officer (Worker A)** or the **Cashier (Worker B)**. 

This code does exactly that. When a user asks a question, the **Supervisor AI** decides whether it's a math question or an employee leave-balance question, and then routes it to the specialized **Worker AI** that knows how to handle it.

---

## 2. The Shared Memory: `state.py`
For multiple agents to talk to each other, they need a shared notepad to pass information around. 
```python
class SupervisorWorkerState(TypedDict, total=False):
    query: str         # The user's original question
    worker: str        # The worker chosen by the supervisor
    expression: str    # Used by math worker to store the formula
    result: str        # The final answer
```
This is a dictionary that gets passed from agent to agent. The Supervisor reads the `query` and writes down the `worker`. The Worker reads the `query` and writes down the `result`.

---

## 3. The Brains (Agents): `nodes.py`
This file contains the logic for your three AIs (nodes).

* **The Supervisor (`supervisor`):**
  It takes the user's query and uses a prompt to ask the LLM (Large Language Model) to output exactly one word: `math` or `leave`. It then saves this choice in the state as `worker`.
* **The Math Worker (`math_agent`):**
  If routed here, this agent asks the LLM to translate the user's question into a Python math expression (e.g., `"10 + 5"`). It then uses your actual `calculator` tool to run the math and saves the output in `result`.
* **The Leave Worker (`leaves_balance`):**
  If routed here, this agent asks the LLM to extract just the employee's name (e.g., `"Alice"`). It then calls the `get_leave_balance` tool (which talks to your SQLite database) to get her remaining leave days, and saves it in `result`.

---

## 4. The Workflow Map: `graph.py`
This file uses **LangGraph** to draw the map connecting your agents. 
```python
    # 1. Add the agents to the map
    graph.add_node("supervisor", supervisor)
    graph.add_node("math_agent", math_agent)
    graph.add_node("leaves_balance", leaves_balance)

    # 2. Tell the system to ALWAYS start at the supervisor
    graph.set_entry_point("supervisor")

    # 3. Create the routing logic (Conditional Edges)
    graph.add_conditional_edges(
        "supervisor",
        route, # This function just looks at state["worker"]
        {
            "math": "math_agent",
            "leave": "leaves_balance",
        }
    )
```
This tells LangGraph: *"Start at the supervisor. Whatever the supervisor outputs (`math` or `leave`), follow that path to the next agent. When that agent is done, the workflow ends."*

---

## 5. The Database Tool: `leaves_db.py`
This is a standard Python SQLite script. It acts as the real-world tool that your Leave Worker uses. 
If the database doesn't exist, `initialize_db()` creates it and adds Alice, Bob, and Charlie with their leave balances. `get_leave_balance("Alice")` simply runs an SQL `SELECT` query to find out how many days she has left.

---

## 6. Putting it all together: `run.py`
This script just tests your system. It sends two queries into the graph:
1. *"What is the square of the average of 10 and 5?"* ➡️ Supervisor sees math ➡️ Math Worker solves it.
2. *"What is the leave balance for Alice?"* ➡️ Supervisor sees leave ➡️ Leave Worker queries the database.

### Summary
The Supervisor-Worker pattern is amazing because it prevents a single AI from getting confused by trying to do too many different things. By delegating tasks to specialized workers equipped with specific tools (like a calculator or a database), the system becomes highly accurate and scalable!
