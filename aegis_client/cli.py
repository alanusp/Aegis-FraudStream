# SPDX-License-Identifier: Apache-2.0
import json, os, sys, argparse
from .client import Client

def main():
    p = argparse.ArgumentParser(prog="aegis")
    p.add_argument("--base", default=os.getenv("AEGIS_BASE","http://127.0.0.1:8080"))
    p.add_argument("--key", default=os.getenv("AEGIS_KEY"))
    sub = p.add_subparsers(dest="cmd", required=True)
    inf = sub.add_parser("infer"); inf.add_argument("user_id"); inf.add_argument("amount", type=float); inf.add_argument("tx_count_1h", type=int); inf.add_argument("country_risk", type=float)
    bat = sub.add_parser("batch"); bat.add_argument("path")
    args = p.parse_args()
    c = Client(args.base, args.key)
    if args.cmd == "infer":
        out = c.inference(args.user_id, args.amount, args.tx_count_1h, args.country_risk)
        print(json.dumps(out, indent=2))
    elif args.cmd == "batch":
        items = json.load(open(args.path,"r",encoding="utf-8"))
        out = c.batch_inference(items)
        print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
