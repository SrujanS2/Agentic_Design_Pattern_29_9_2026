from .graph import build_graph


def run_question(question: str) -> dict:
    """Run the tool-using agent workflow on a single question."""
    app = build_graph()
    return app.invoke({"question": question})


if __name__ == "__main__":
    # --- Math question ---
    result = run_question("What is the square of the average of 10 and 5?")
    print("\n--- Math Question ---")
    print(f"Question : {result['question']}")
    print(f"Category : {result['category']}")
    print(f"Expression: {result.get('expression', 'N/A')}")
    print(f"Result    : {result['result']}")

    # --- General question (fallback) ---
    result = run_question("Define AI")
    print("\n--- General Question ---")
    print(f"Question : {result['question']}")
    print(f"Category : {result['category']}")
    print(f"Result   : {result['result']}")