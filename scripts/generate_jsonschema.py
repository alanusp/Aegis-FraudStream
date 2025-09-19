# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import json, pathlib
from aegis_fraudstream import schemas
out = pathlib.Path(__file__).resolve().parents[1]/"docs"/"schemas"
out.mkdir(parents=True, exist_ok=True)
try:
    Event = getattr(schemas, "Event")
    out.joinpath("event.schema.json").write_text(json.dumps(Event.model_json_schema(), indent=2))
    print("Wrote docs/schemas/event.schema.json")
except Exception as e:
    print("Schema generation skipped:", e)
