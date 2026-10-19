import json, subprocess, sys

domain, role = sys.argv[1], sys.argv[2]
acct = subprocess.check_output(["aws", "sts", "get-caller-identity", "--query", "Account", "--output", "text"], text=True).strip()
cur = json.loads(subprocess.check_output(["aws", "opensearch", "describe-domain-config", "--domain-name", domain, "--query", "DomainConfig.AccessPolicies.Options", "--output", "text"], text=True))
cur["Statement"].append({
    "Effect": "Allow",
    "Principal": {"AWS": f"arn:aws:iam::{acct}:role/{role}"},
    "Action": "es:*",
    "Resource": f"arn:aws:es:us-east-1:{acct}:domain/{domain}/*"
})
sys.stdout.write(json.dumps(cur))