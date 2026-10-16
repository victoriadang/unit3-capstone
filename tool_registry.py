"""
Day 3 Lab Solution: Connect SQL Agent and Retrieval Agent to a Shared Tool Registry

Standardizes both agents to a consistent interface, builds the registry,
and includes a simple routing-suggestion preview (deliberately limited -
see Part 4 notes on the combined-question test).
"""

import os
from dotenv import load_dotenv
from bedrock_client import invoke_claude
from agents.retrieval_agent import run_retrieval_agent
from agents.sql_agent import run_sql_agent
load_dotenv()

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Part 2: Tool Registry ────────────────────────────────────────────────────

TOOL_REGISTRY = {
    "sql_agent": {
        "function": run_sql_agent,
        "schema": {
            "name": "sql_agent",
            "description": (
                "Query the relational database for structured, numeric, or categorical "
                "data about clients, projects, consultants, and invoices - counts, totals, "
                "statuses, and comparisons. Do not use for policy or procedural questions."
            ),
            "input_schema": {
                "type": "object",
                "properties": {"question": {"type": "string"}},
                "required": ["question"]
            }
        }
    },
    "retrieval_agent": {
        "function": run_retrieval_agent,
        "schema": {
            "name": "retrieval_agent",
            "description": (
                "Search indexed documents for policy, procedure, and case study information - "
                "onboarding, expense guidelines, or project narratives. Do not use for "
                "structured numeric or database questions."
            ),
            "input_schema": {
                "type": "object",
                "properties": {"question": {"type": "string"}},
                "required": ["question"]
            }
        }
    }
}


def get_all_schemas() -> list:
    return [tool["schema"] for tool in TOOL_REGISTRY.values()]


def call_tool(tool_name: str, question: str) -> dict:
    if tool_name not in TOOL_REGISTRY:
        return {"success": False, "answer": f"Unknown tool: {tool_name}", "sources": [], "metadata": {}}
    return TOOL_REGISTRY[tool_name]["function"](question)


# ── Part 4: Simple Routing Preview ──────────────────────────────────────────

def suggest_tool(question: str) -> str:
    schemas_description = "\n".join([f"- {s['name']}: {s['description']}" for s in get_all_schemas()])

    prompt = (
        f"Available tools:\n{schemas_description}\n\n"
        f"Question: {question}\n\n"
        "Which tool should handle this? Reply with only the tool name."
    )
    result = invoke_claude(prompt, max_tokens=500)
    return result["text"].strip()


if __name__ == "__main__":
    print("=" * 70)
    print("PART 3: Registry Direct Tests")
    print("=" * 70)
    print("Registered tools:", [s["name"] for s in get_all_schemas()])

    result1 = call_tool("sql_agent", "How many active projects do we have?")
    print("\nSQL agent test:", result1)

    result2 = call_tool("retrieval_agent", "What is our onboarding process?")
    print("\nRetrieval agent test:", result2)

    result3 = call_tool("nonexistent_tool", "test")
    print("\nUnknown tool test:", result3)

    print("\n" + "=" * 70)
    print("PART 4: Routing Suggestion Preview")
    print("=" * 70)
    for q in [
        "How many consultants do we have on active projects?",
        "What is our expense reimbursement policy?",
        "How many active projects do we have and what's our onboarding process?",
    ]:
        print(f"\nQ: {q}")
        print(f"Suggested tool: {suggest_tool(q)}")