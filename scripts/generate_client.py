# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import subprocess, sys, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
openapi = root / "docs" / "openapi.gen.yaml"
outdir = root / "clients" / "python"
outdir.mkdir(parents=True, exist_ok=True)
subprocess.check_call([sys.executable,"-m","pip","install","openapi-python-client"])
subprocess.check_call(["openapi-python-client","generate","--path", str(openapi), "--output-path", str(outdir), "--meta","name=AegisClient"])
print("Client generated at", outdir)
