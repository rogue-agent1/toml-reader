# toml-reader

TOML parser and query tool. Zero dependencies (Python 3.11+).

## Usage

```bash
# Print entire file as JSON
python3 toml_reader.py config.toml

# Query specific key
python3 toml_reader.py config.toml server.port

# List top-level keys
python3 toml_reader.py config.toml --keys

# Flatten to dotted keys
python3 toml_reader.py config.toml --flat
```
