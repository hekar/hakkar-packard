# test-env

A CLI application built with Python.

## Installation

This project uses `uv` for dependency management. To install:

```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
uv pip install -e .
```

## Usage

After installation, you can use the CLI command:

```bash
test-env
```

## Development

To set up the development environment:

1. Create a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   ```

2. Install development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

## License

MIT License 