#!/usr/bin/env python3
"""toml_reader - TOML parser and query tool. Zero dependencies (Python 3.11+ tomllib)."""
import sys, json

try:
    import tomllib
except ImportError:
    import tomli as tomllib

def read_toml(path):
    with open(path, "rb") as f:
        return tomllib.load(f)

def query(data, path):
    keys = path.split(".")
    cur = data
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        elif isinstance(cur, list):
            try:
                cur = cur[int(k)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return cur

def fmt(val):
    if isinstance(val, (dict, list)):
        return json.dumps(val, indent=2, default=str)
    return str(val)

def usage():
    print("""toml_reader - TOML parser and query tool

Usage:
  toml_reader <file>                 Print entire file as JSON
  toml_reader <file> <key.path>      Query a specific key
  toml_reader <file> --keys          List top-level keys
  toml_reader <file> --flat          Flatten to dotted keys

Examples:
  toml_reader config.toml
  toml_reader config.toml server.port
  toml_reader config.toml --keys""")

def flatten(data, prefix=""):
    items = []
    for k, v in data.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            items.extend(flatten(v, key))
        else:
            items.append((key, v))
    return items

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        usage(); sys.exit(0)
    path = args[0]
    try:
        data = read_toml(path)
        if len(args) == 1:
            print(json.dumps(data, indent=2, default=str))
        elif args[1] == "--keys":
            for k in data.keys():
                print(k)
        elif args[1] == "--flat":
            for k, v in flatten(data):
                print(f"{k} = {fmt(v)}")
        else:
            result = query(data, args[1])
            if result is None:
                print(f"Key not found: {args[1]}", file=sys.stderr); sys.exit(1)
            print(fmt(result))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); sys.exit(1)
