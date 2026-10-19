"""
Lab Solution: Build a SQL Query Agent Against Your Day 1 RDS Schema

Uses the sample consulting-firm schema from the Day 1 RDS Setup lab:
clients, projects, consultants, invoices.

Calls Claude via Bedrock (see bedrock_client.py) rather than the direct
Anthropic SDK — students in this environment don't have direct Anthropic
API keys.
"""

import psycopg2
import os
from dotenv import load_dotenv
from bedrock_client import invoke_claude
load_dotenv()

# ── Part 1: Schema Context ──────────────────────────────────────────────────

SCHEMA_CONTEXT = """
Tables available:
- clients(id, name, industry, region, contract_value, created_date)
  - region is one of: 'North', 'South', 'East', 'West'
  - contract_value is in USD
- projects(id, client_id, name, status, start_date, end_date, budget)
  - status is one of: 'active', 'completed', 'on-hold'
  - budget is in USD
  - client_id references clients.id
- consultants(id, name, grade, specialisation, project_id, billable_hours)
  - grade is one of: 'Analyst', 'Senior', 'Manager', 'Director'
  - project_id references projects.id
- invoices(id, project_id, amount, status, due_date, paid_date)
  - status is one of: 'paid', 'pending', 'overdue'
  - amount is in USD
  - project_id references projects.id

All dates are in ISO 8601 format (YYYY-MM-DD).
"""


# ── Part 2: Query Generation ────────────────────────────────────────────────

def generate_sql(question: str) -> str:
    prompt = (
        f"{SCHEMA_CONTEXT}\n\n"
        f"Generate a SQL query to answer: {question}\n\n"
        "Return ONLY the SQL query. No explanation, no markdown, no backticks."
    )
    result = invoke_claude(prompt, max_tokens=512, component="sql_generation")
    sql = result["text"].strip()
    # Strip markdown code fences if Claude adds them despite instructions
    sql = sql.removeprefix("```sql").removeprefix("```").removesuffix("```").strip()
    return sql


# ── Part 3: Query Execution (unsafe version — validation added in Lab 3) ──

def execute_query(sql: str) -> dict:
    try:
        conn = psycopg2.connect(
            host=os.getenv("RDS_HOST"), port=int(os.getenv("RDS_PORT")),
            dbname=os.getenv("RDS_DATABASE"), user=os.getenv("RDS_USER"),
            password=os.getenv("RDS_PASSWORD")
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        conn.close()
        return {"success": True, "columns": cols, "rows": rows}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── Part 4: Full Agent ──────────────────────────────────────────────────────

def sql_agent(question: str) -> str:
    sql = generate_sql(question)
    result = execute_query(sql)

    if not result["success"]:
        return f"Query failed: {result['error']}\nGenerated SQL was: {sql}"

    prompt = (
        f"The user asked: {question}\n"
        f"SQL used: {sql}\n"
        f"Columns: {result['columns']}\n"
        f"Data: {result['rows'][:20]}\n\n"
        "Provide a clear, concise natural-language answer based on this data."
    )
    interpretation = invoke_claude(prompt, max_tokens=500)
    return interpretation["text"]


# ── Part 5: Agent with Memory ───────────────────────────────────────────────

def sql_agent_with_memory(question: str, history: list) -> tuple[str, list]:
    context_summary = "\n".join([f"Q: {h['question']}\nA: {h['answer']}" for h in history])

    sql_prompt = (
        f"{SCHEMA_CONTEXT}\n\n"
        f"Conversation so far:\n{context_summary}\n\n"
        f"New question (may refer back to the conversation above): {question}\n\n"
        "Generate ONLY a SQL query to answer the new question."
    )
    sql_result = invoke_claude(sql_prompt, max_tokens=512)
    sql = sql_result["text"].strip()
    sql = sql.removeprefix("```sql").removeprefix("```").removesuffix("```").strip()

    result = execute_query(sql)
    if not result["success"]:
        answer = f"Query failed: {result['error']}"
    else:
        answer_prompt = f"Question: {question}\nData: {result['rows'][:20]}\n\nAnswer concisely."
        answer_result = invoke_claude(answer_prompt, max_tokens=500)
        answer = answer_result["text"]

    history.append({"question": question, "answer": answer})
    return answer, history


# # ── Test Suite: 8 Questions of Increasing Complexity ────────────────────────

# if __name__ == "__main__":
#     test_questions = [
#         "How many clients do we have?",                                          # 1. simple count
#         "What is Acme Corp's contract value?",                                   # 2. simple lookup
#         "Which consultants are working on active projects?",                     # 3. requires join
#         "What is the total budget across all active projects?",                  # 4. aggregation
#         "Show me all invoices with status overdue",                              # 5. WHERE clause
#         "What is the average billable hours per project, by project name?",      # 6. join + aggregation
#         "Show me our best clients",                                              # 7. ambiguous on purpose
#         "What is our current stock price?",                                      # 8. cannot be answered
#     ]

#     print("=" * 70)
#     print("PART 4: Full Agent Test — 8 Questions")
#     print("=" * 70)
#     for q in test_questions:
#         print(f"\nQ: {q}")
#         print(f"A: {sql_agent(q)}")

#     print("\n" + "=" * 70)
#     print("PART 5: Memory Test — Follow-Up Question")
#     print("=" * 70)
#     history = []
#     a1, history = sql_agent_with_memory("How many active projects does Acme Corp have?", history)
#     print(f"\nQ1: How many active projects does Acme Corp have?\nA1: {a1}")

#     a2, history = sql_agent_with_memory("What about their total contract value?", history)
#     print(f"\nQ2: What about their total contract value?\nA2: {a2}")


# ── Part 1: Validator ────────────────────────────────────────────────────────


BLOCKED_KEYWORDS = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE",
                    "EXEC", "EXECUTE", "GRANT", "REVOKE"]


def validate_sql(query: str) -> dict:
    """
    Validates a Claude-generated SQL query before execution.
    Blocks any query that is not a SELECT or contains destructive keywords.
    Uses word-boundary matching to avoid false positives on column names
    like 'deleted_at'.
    """
    query_upper = query.upper().strip()
    padded = f" {query_upper} "

    for keyword in BLOCKED_KEYWORDS:
        if f" {keyword} " in padded or query_upper.startswith(keyword + " ") or query_upper == keyword:
            return {
                "valid": False,
                "reason": f"Blocked: '{keyword}' is not permitted. Only SELECT queries are allowed."
            }

    if not query_upper.startswith("SELECT"):
        return {
            "valid": False,
            "reason": "Only SELECT queries are permitted. Query must begin with SELECT."
        }

    # Block stacked queries (multiple statements separated by semicolons)
    # A single trailing semicolon is fine; anything after it is not.
    stripped = query.strip().rstrip(";")
    if ";" in stripped:
        return {
            "valid": False,
            "reason": "Blocked: multiple statements detected (possible stacked query attempt)."
        }

    return {"valid": True, "reason": "OK"}


# ── Part 2: Test Suite ───────────────────────────────────────────────────────
#
# NOTE: the original stacked-query test case
# ("SELECT * FROM projects; DROP TABLE clients;") is blocked by the
# BLOCKED_KEYWORDS check (it contains "DROP") before the code ever reaches
# the dedicated semicolon/stacking check — verified directly by running
# validate_sql() on it in isolation. That means the semicolon-detection
# logic itself was never actually exercised by this test suite; a bug in
# just that logic could have shipped undetected. Added a stacked query
# using only harmless keywords, which does hit the semicolon check
# specifically, plus a single-trailing-semicolon case to confirm that
# documented "one trailing semicolon is fine" behavior actually holds.

TEST_CASES = [
    ("SELECT * FROM clients WHERE region = 'North'", True),
    ("select count(*) from projects", True),
    ("SELECT name, contract_value FROM clients ORDER BY contract_value DESC LIMIT 5", True),
    ("DROP TABLE clients", False),
    ("DELETE FROM projects WHERE status = 'active'", False),
    ("UPDATE consultants SET grade = 'Senior'", False),
    ("INSERT INTO invoices VALUES (1, 100, 'paid')", False),
    ("SELECT * FROM projects; DROP TABLE clients;", False),
    ("SeLeCt * FrOm clients", True),          # mixed case, still valid SELECT
    ("SELECT deleted_at FROM projects", True), # column name contains 'delete' but isn't the keyword
    ("SELECT * FROM projects; SELECT * FROM clients", False),  # stacked query, no blocked keyword —
                                                                # this is the one that actually proves
                                                                # the semicolon check works on its own
    ("SELECT * FROM clients;", True),          # single trailing semicolon should still be valid
]


def run_test_suite():
    print("=" * 70)
    print("VALIDATOR TEST SUITE")
    print("=" * 70)
    all_passed = True
    for query, expected in TEST_CASES:
        result = validate_sql(query)
        passed = result["valid"] == expected
        all_passed = all_passed and passed
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] valid={result['valid']} (expected {expected}) | {query[:60]}")
    print(f"\nAll tests passed: {all_passed}")
    return all_passed


# ── Part 3: Wired-In Validated Agent ─────────────────────────────────────────

def generate_sql(question: str) -> str:
    prompt = (
        f"{SCHEMA_CONTEXT}\n\n"
        f"Generate a SQL query to answer: {question}\n\n"
        "Return ONLY the SQL query. No explanation, no markdown, no backticks."
    )
    result = invoke_claude(prompt, max_tokens=512, component="sql_generation")
    sql = result["text"].strip()
    return sql.removeprefix("```sql").removeprefix("```").removesuffix("```").strip()


def execute_query_safely(sql: str) -> dict:
    validation = validate_sql(sql)

    if not validation["valid"]:
        return {
            "success": False,
            "error": validation["reason"],
            "validation": "BLOCKED",
            "sql": sql
        }

    try:
        conn = psycopg2.connect(
            host=os.getenv("RDS_HOST"), port=int(os.getenv("RDS_PORT")),
            dbname=os.getenv("RDS_DATABASE"), user=os.getenv("RDS_USER"),
            password=os.getenv("RDS_PASSWORD")
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        conn.close()
        return {
            "success": True, "columns": cols, "rows": rows,
            "validation": "PASSED", "sql": sql
        }
    except Exception as e:
        return {"success": False, "error": str(e), "validation": "EXECUTION_ERROR", "sql": sql}


# def validated_sql_agent(question: str) -> dict:
#     sql = generate_sql(question)
#     result = execute_query_safely(sql)

#     if not result["success"]:
#         return {
#             "answer": f"Query blocked or failed: {result['error']}",
#             "sql": sql,
#             "validation": result["validation"]
#         }

#     prompt = (
#         f"Question: {question}\nColumns: {result['columns']}\n"
#         f"Data: {result['rows'][:20]}\n\nAnswer concisely."
#     )
#     interpretation = invoke_claude(prompt, max_tokens=500)

#     return {"answer": interpretation["text"], "sql": sql, "validation": result["validation"]}


def run_sql_agent(question: str) -> dict:
    sql = None
    try:
        sql = generate_sql(question)
        result = execute_query_safely(sql)

        if not result["success"]:
            return{
                "success": False,
                "answer": f"Query blocked or failed: {result['error']}",
                "sources": [f"SQL: {sql}"],
                "metadata": {"validation": result["validation"], "row_count": 0},
            }
        prompt = (
            f"Question: {question}\nColumns: {result['columns']}\n"
            f"data: {result['rows'][:20]}\n\nAnswer concisely."
        )
        interpretation = invoke_claude(prompt, max_tokens=500, component="sql_interpretation")

        return {
            "success": True,
            "answer": interpretation["text"],
            "sources": [f"SQL: {sql}"],
            "metadata": {
                "validation": result["validation"],
                "row_count":len(result["rows"])
            },
    }

    except Exception as e:
        return {
        "success": False,
        "answer": f"Error: {e}",
        "sources": [f"SQL: {sql}"] if sql else [],
        "metadata": {"validation": "ERROR", "error_type": type(e).__name__, "row_count": 0},

    }


if __name__ == "__main__":
    run_test_suite()

    print("\n" + "=" * 70)
    print("RE-TESTING LAB 2 FAILURE MODES AGAINST THE VALIDATED AGENT")
    print("=" * 70)

    # NOTE: the two "direct attempt" rows below (DROP and the stacked query)
    # were originally re-tested by passing the malicious string as the
    # natural-language *question* to validated_sql_agent(), e.g.
    # validated_sql_agent("DROP TABLE clients"). That doesn't actually test
    # the validator: Claude refuses to generate destructive SQL from that
    # prompt and instead returns a harmless SELECT of its own, so
    # validate_sql() never sees a DROP or a stacked query at all — verified
    # directly (generate_sql("DROP TABLE clients") produced
    # "SELECT 'This request is not allowed...' AS error_message;", which
    # validate_sql() correctly marked valid, because it *is* valid). The
    # findings table's claim that these were "blocked by the validator" was
    # therefore wrong — the real blocker was Claude's own alignment at the
    # generation step, not this lab's validation layer, and the two were
    # never actually distinguished.
    #
    # To genuinely test whether the validator blocks a destructive query
    # reaching the database, the malicious SQL needs to go straight to
    # execute_query_safely() — simulating the real threat model (Claude
    # eventually *does* generate something destructive) rather than asking
    # Claude in English to do something it already refuses to do.
    ambiguous_questions = [
        "Which client is our best client?",              # #1 — ambiguous, not a validation problem
        "Which projects started recently?",               # #2 — ambiguous, not a validation problem
        "What's the status of things?",                   # #3 — ambiguous, not a validation problem
        "Show me everything",                             # #6 — unbounded, not caught by SQL validation alone
    ]
    for q in ambiguous_questions:
        result = run_sql_agent(q)
        print(f"\nQ: {q}")
        print(f"Validation: {result['metadata']['validation']}")
        print(f"Answer: {result['answer']}")

    direct_attacks = [
        "DROP TABLE clients",                             # direct attempt — should be blocked
        "SELECT * FROM projects; DROP TABLE clients;",    # stacked query attempt — should be blocked
    ]
    for sql in direct_attacks:
        result = execute_query_safely(sql)
        print(f"\nSQL fed directly to execute_query_safely(): {sql!r}")
        print(f"Validation: {result['validation']}")
        print(f"Error/result: {result.get('error', result.get('rows'))}")

    print("\n" + "=" * 70)
    print("CONFIRMING LEGITIMATE QUESTIONS STILL WORK")
    print("=" * 70)
    legit_questions = [
        "How many active projects do we have?",
        "What is the total contract value across all clients?",
    ]
    for q in legit_questions:
        result = run_sql_agent(q)
        print(f"\nQ: {q}")
        print(f"Validation: {result['metadata']['validation']}")
        print(f"Answer: {result['answer']}")