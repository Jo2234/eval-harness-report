import argparse, hashlib, json, statistics, time
from pathlib import Path
import httpx

parser = argparse.ArgumentParser(
    description="Alternating local API timing after both targets complete identical workloads"
)
parser.add_argument("--before-api", default="http://127.0.0.1:8766")
parser.add_argument("--after-api", default="http://127.0.0.1:8767")
parser.add_argument("--before-ingestion", type=Path, required=True)
parser.add_argument("--after-ingestion", type=Path, required=True)
parser.add_argument("--results", type=Path, required=True)
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
suite = json.loads(args.results.read_text())["results"]
selected = [
    next(r for r in suite if r["case_id"].endswith(s)) for s in ["001", "027", "031"]
]
targets = {
    "before": (args.before_api, args.before_ingestion),
    "after": (args.after_api, args.after_ingestion),
}
companies = {k: json.loads(v[1].read_text())["companies"] for k, v in targets.items()}
records = []
with httpx.Client(timeout=90, trust_env=False) as client:
    for trial in range(6):
        for case in selected:
            for target in (
                ["before", "after"] if trial % 2 == 0 else ["after", "before"]
            ):
                start = time.perf_counter()
                response = client.post(
                    targets[target][0] + "/research/chat",
                    json={
                        "question": case["question"],
                        "company_ids": [
                            companies[target][t]
                            for t in case["case_definition"]["company_ids"]
                        ],
                        "top_k": 8,
                    },
                )
                response.raise_for_status()
                elapsed = (time.perf_counter() - start) * 1000
                if trial:
                    records.append(
                        {
                            "trial": trial,
                            "case_id": case["case_id"],
                            "target": target,
                            "latency_ms": round(elapsed, 3),
                            "answer_sha256": hashlib.sha256(
                                response.json()["answer"].encode()
                            ).hexdigest(),
                        }
                    )
summary = {
    k: {
        "n": sum(r["target"] == k for r in records),
        "median_ms": statistics.median(
            r["latency_ms"] for r in records if r["target"] == k
        ),
        "max_ms": max(r["latency_ms"] for r in records if r["target"] == k),
    }
    for k in targets
}
result = {
    "method": "One warmup then five repeats of three fixed questions, alternating target order. Same corpus/settings, loopback HTTP, growing histories; both APIs have completed the same 50 questions. This is a small local timing check, not a load benchmark.",
    "summary": summary,
    "records": records,
}
args.out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(summary))
