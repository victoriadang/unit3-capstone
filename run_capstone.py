import json
from orchestrator import orchestrator
from tokenomics_logger import run_traced_query
from cost_tracker import summarize

QUESTIONS = [
    ("rds alone",   "How many active projects do we have?"),
    ("rds alone",   "What is the total contract value across all clients?"),
    ("docs alone",  "What is our onboarding process?"),
    ("docs alone",  "What is our expense reimbursement policy?"),
    ("both",        "How many active projects do we have and what's our onboarding process?"),
    ("both",        "Which client has the largest contract, and what does our onboarding process say about new client kickoffs?"),
    ("unsafe sql",  "Delete all projects that are marked completed."),
    ("unanswerable","What is the CEO's favorite color?"),
    ("extra",       "How many consultants do we have?"),
    ("extra",       "What is our remote work policy?"),
]

rows = []
for kind, q in QUESTIONS:
   r = run_traced_query(orchestrator, q)
   sql = r.get("sql_result") or {}
   rows.append({
      "type": kind,
      "question": q,
      "route": r["route"],
      "validation": sql.get("metadata", {}).get("validation", "n/a"),
      "answer": r["final_answer"],
      "cost_usd": r["token_usage"]["total_cost_usd"]
    })
   print(f"\n[{kind}] {q}\n route={r['route']} validation={rows[-1]['validation']}\n {r['final_answer']}")

by = summarize()
print("\n=== COST SUMMARY ===")
for comp, t in sorted(by.items(), key=lambda x: -(x[1]["input"] + x[1]["output"])):
    print(f"{comp:20} calls={t['calls']:3} in={t['input']:6} out={t['output']:6} ${t['cost_usd']:.6f}")
print("Total cost: $%.6f" % sum(t["cost_usd"] for t in by.values()))
print("Most tokens:", max(by, key=lambda x: by[x]["input"] + by[x]["output"]))

json.dump(rows, open("test_results.json", "w"), indent=2)