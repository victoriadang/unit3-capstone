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
                "Query the relational database (clients, projects, consultants, and invoices) for structured "
                "data: counts, totals, averages, budgets, invoice amounts and payment status, project stauses "
                "and dates, consultant assignments. Use for any questions answered by numbers or records. "
                "NOT for policies, processess, how-to guidance, or narrative content from documents. "
                "Read-only: never modifies data."
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
                "Search indexed company documents for (onboarding process, expenses "
                "and remote work policies, cloud migration playbook, client reports) "
                "and answer with citations. Use for any policy, procedure, and 'how do we..' "
                "questions, and for project narratives. NOT for counts, totals, budgets, or "
                "records stored in the database. If a question needs both numbers and documents, "
                "both tools apply."
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
    result = invoke_claude(prompt, max_tokens=500, component="classification")
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