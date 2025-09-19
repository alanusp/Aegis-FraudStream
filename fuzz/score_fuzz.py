# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
import atheris, json, sys
from aegis_fraudstream.schemas import Event
with atheris.instrument_imports(): pass
def TestOneInput(data: bytes):
    try:
        s = data.decode("utf-8", "ignore")
        d = json.loads(s)
        Event.model_validate(d)  # may raise; we only care about crashes
    except Exception:
        pass
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()
if __name__ == "__main__":
    main()
