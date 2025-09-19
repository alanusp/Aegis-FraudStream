# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
import sys, json, pathlib, yaml  # type: ignore
from typing import Dict, Any

def load(path: pathlib.Path) -> Dict[str, Any]:
    t = path.read_text()
    if path.suffix in (".yaml", ".yml"):
        return yaml.safe_load(t)
    return json.loads(t)

def main(prev_path: str, new_path: str) -> int:
    prev = load(pathlib.Path(prev_path))
    new = load(pathlib.Path(new_path))
    errors = []
    # Removed paths or methods
    for p, ops in prev.get("paths", {}).items():
        if p not in new.get("paths", {}):
            errors.append(f"Removed path: {p}")
            continue
        for m in ops.keys():
            if m not in new["paths"][p]:
                errors.append(f"Removed operation: {m} {p}")
    if errors:
        print("\n".join(errors))
        return 1
    print("No breaking removals detected")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
