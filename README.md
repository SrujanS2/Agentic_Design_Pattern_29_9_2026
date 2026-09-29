# 🤖 Agentic Design Pattern – Tool-Using Agent

A hands-on implementation of the **Tool-Using** agentic design pattern built with
**LangGraph**, **LangChain**, and **Streamlit**.

The agent intelligently **classifies** every incoming question and **routes** it to
the appropriate handler:

| Category | Handler | Description |
|---|---|---|
| 🔢 **Math** | `math_agent` (calculator tool) | Converts the question into a Python expression and evaluates it |
| 💡 **General** | `general_agent` (LLM fallback) | Answers general-knowledge questions directly via the LLM |

---

## 📂 Project Structure

```
Agentic_Design_Pattern_29_9_2026/
├── app.py                          # Streamlit frontend
├── config/
│   └── llm.py                      # LLM configuration (OpenAI GPT-4o-mini)
├── patterns/
│   └── tool_using/
│       ├── state.py                # AgentState definition
│       ├── nodes.py                # Agent nodes (reasoning, math, general)
│       ├── graph.py                # LangGraph workflow with conditional routing
│       └── run.py                  # CLI runner & reusable run_question()
├── tools/
│   └── calculator.py               # Calculator tool (eval-based)
├── requirements.txt
├── .env                            # API keys (not committed)
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🏗️ Architecture

```
                    ┌─────────────────────┐
                    │   User Question     │
                    └────────┬────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │     reasoning_agent        │
                │  (classify → MATH/GENERAL) │
                └─────┬──────────────┬───────┘
                      │              │
               MATH   │              │  GENERAL
                      ▼              ▼
            ┌──────────────┐  ┌──────────────┐
            │  math_agent  │  │ general_agent│
            │ (calculator) │  │  (LLM reply) │
            └──────┬───────┘  └──────┬───────┘
                   │                 │
                   ▼                 ▼
                ┌────────────────────────┐
                │        Result          │
                └────────────────────────┘
```

**Key design decision** — The `reasoning_agent` uses **conditional edges**
(`add_conditional_edges`) in LangGraph. This means the workflow dynamically
picks the right downstream node rather than forcing every question through
the calculator.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- An [OpenAI API key]<your_api_key>

### 1. Clone the repository

```bash
git clone https://github.com/SrujanS2/Agentic_Design_Pattern_29_9_2026.git
cd Agentic_Design_Pattern_29_9_2026
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-key-here
```

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**.

### Alternative: Run from CLI

```bash
python -m patterns.tool_using.run
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `langgraph` | Stateful agent workflow orchestration |
| `langchain` | LLM abstraction and prompt management |
| `langchain-openai` | OpenAI model integration |
| `python-dotenv` | Load `.env` variables |
| `streamlit` | Interactive web frontend |

---

## 🔧 How It Works

1. **`reasoning_agent`** receives the user's question and uses GPT-4o-mini to
   classify it as `MATH` or `GENERAL`.
   - If **MATH**, it also extracts a valid Python math expression.
   - If **GENERAL**, it flags the question for the fallback path.

2. **`route_question`** (conditional edge) inspects `state["category"]` and
   directs the flow to the appropriate node.

3. **`math_agent`** passes the expression to `calculator()`, which safely
   evaluates it and returns the numeric result.

4. **`general_agent`** sends the original question to the LLM and returns a
   natural-language answer.

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).
