"""
lambda_handler.py -- wraps the orchestrator in the format Lambda expects.
"""
import json
from orchestrator import orchestrator
from tokenomics_logger import run_traced_query


def handler(event, context):
    try:
        body = event.get("body", event)
        if isinstance(body, str):
            body = json.loads(body)
        question = (body.get("question") or"").strip()
        if not question:
            return {"statusCode": 400, "body": json.dumps({"error": "question is required"})}


        result = run_traced_query(orchestrator, question)
        sql_validation = result.get("sql_result") or {}
        payload = {
            "question": question,
            "route": result.get("route"),
            "sql_validation": (sql.get("metadata") or {}).get("validation"),
            "answer": result.get("final_answer"),
            "token_usage": result.get("token_usage"),
        }

        return {
            "statusCode": 200,
            "body": json.dumps(payload, default=str),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
