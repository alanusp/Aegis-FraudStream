# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
from fastapi.openapi.utils import get_openapi
from aegis_fraudstream.app import app
import yaml, sys
schema = get_openapi(title=app.title, version=app.version, routes=app.routes)
yaml.safe_dump(schema, sys.stdout, sort_keys=False)

# Supports YAML (stdout) and JSON via --json flag
