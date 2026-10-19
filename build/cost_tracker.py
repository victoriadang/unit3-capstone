CALL_LOG = []

PRICE_PER_M = {"input": 3.00, "output": 15.00}

def record_usage(component, input_tokens, output_tokens):
    cost = (input_tokens * PRICE_PER_M["input"]
            + output_tokens * PRICE_PER_M["output"]) / 1_000_000
    CALL_LOG.append({
        "component": component,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": cost
    })
    print(f"[COST] {component}: {input_tokens} input tokens, {output_tokens} output tokens, cost ${cost:.6f}")

def summarize(calls=None):
    by = {}
    for c in (CALL_LOG if calls is None else calls):
        t = by.setdefault(c["component"],
                         {"calls": 0, "input": 0, "output": 0, "cost_usd": 0.0})
        t["calls"] += 1
        t["input"] += c.get("input", c.get("input_tokens", 0))
        t["output"] += c.get("output", c.get("output_tokens", 0))
        t["cost_usd"] += c.get("cost_usd", 0.0)
    return by