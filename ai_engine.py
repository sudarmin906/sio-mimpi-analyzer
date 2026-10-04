import os, json, re
from openai import OpenAI

def enabled():
    return bool(os.environ.get("OPENAI_API_KEY"))

def rank(history, deterministic, mapping, audit=None):
    if not enabled():
        return None
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.environ.get("OPENAI_MODEL", "gpt-6-luna")
    candidates = []
    for x in [deterministic.get("main")] + deterministic.get("backups", []) + deterministic.get("candidates", []):
        if x and re.fullmatch(r"\d{2}", str(x)) and x not in candidates:
            candidates.append(str(x))
    payload = {
        "cutoff": history[-1][1] if history else None,
        "recent_history": [{"period": p, "result": r} for p, r in history[-50:]],
        "mapping": mapping,
        "candidate_pool": candidates,
        "deterministic_prediction": deterministic,
        "previous_audit": audit,
        "method": [
            "Audit previous prediction first",
            "3 forward 2D pairs and 3 reverse pairs",
            "SIO/Mimpi semantic mapping",
            "historical relation and position",
            "Pair Assembly",
            "Eliminated Recovery",
            "Anti-Chasing",
            "No look-ahead"
        ],
        "output": "Return JSON only: main, backups, bbfs, explanation. main must be one candidate; backups exactly four candidates; bbfs exactly six distinct digits. Never invent a candidate."
    }
    response = client.responses.create(
        model=model,
        input=[{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}]
    )
    text = getattr(response, "output_text", "") or ""
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return None
    data = json.loads(match.group(0))
    main = str(data.get("main", ""))
    backups = [str(x) for x in data.get("backups", [])]
    if main not in candidates or not re.fullmatch(r"\d{2}", main):
        return None
    backups = list(dict.fromkeys([x for x in backups if x in candidates and x != main]))[:4]
    if len(backups) != 4:
        return None
    bbfs = "".join(dict.fromkeys([x for x in str(data.get("bbfs", "")) if x.isdigit()]))
    for x in main + "".join(backups):
        if x not in bbfs:
            bbfs += x
    return {"main": main, "backups": backups, "bbfs": bbfs[:6],
            "candidates": candidates, "explanation": str(data.get("explanation", "")), "model": model}
