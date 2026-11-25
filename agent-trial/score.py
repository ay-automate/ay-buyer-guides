"""Compare observations from the sandbox with the supplied answer key."""
import json
import sys
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


if len(sys.argv) != 2:
    sys.exit("Usage: python3 score.py observed.json")
try:
    expected = load(Path(__file__).with_name("reference.json"))
    observed = load(sys.argv[1])
except (ValueError, OSError) as error:
    sys.exit(str(error))
if not isinstance(observed, dict) or observed.keys() != expected.keys():
    sys.exit("Include exactly these case IDs: " + ", ".join(expected))
passed = 0
for case, target in expected.items():
    result = observed[case]
    if not isinstance(result, dict) or result.keys() != target.keys():
        print(f"FAIL {case}: missing or unexpected fields")
        continue
    differences = [field for field in target
                   if json.dumps(result[field], sort_keys=True) != json.dumps(target[field], sort_keys=True)]
    if differences:
        print(f"FAIL {case}: " + ", ".join(differences))
    else:
        print(f"PASS {case}")
        passed += 1
print(f"{passed}/{len(expected)} cases passed")
sys.exit(int(passed != len(expected)))
