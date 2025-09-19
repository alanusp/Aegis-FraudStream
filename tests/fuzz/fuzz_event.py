# SPDX-License-Identifier: Apache-2.0
import atheris, sys, json
with atheris.instrument_imports():
    from aegis_fraudstream.schemas import Event

def TestOneInput(data: bytes):
    try:
        s = data.decode("utf-8", errors="ignore")
        js = json.loads(s)
        Event.model_validate(js)  # ensure parser robustness
    except Exception:
        pass

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
