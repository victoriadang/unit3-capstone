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
    