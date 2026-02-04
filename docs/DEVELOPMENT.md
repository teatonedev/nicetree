# Development Guide

This guide helps developers set up and contribute to nicetree.

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- git

### Development Installation

1. Clone the repository:
```bash
git clone https://github.com/teatonedev/nicetree.git
cd nicetree
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e ".[dev]"
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Run with coverage:

```bash
pip install pytest-cov
pytest tests/ --cov=nicetree --cov-report=html
```

## Code Style

This project follows PEP 8. Use tools like:

```bash
# Format code
pip install black
black nicetree/ tests/

# Check style
pip install flake8
flake8 nicetree/ tests/

# Type checking
pip install mypy
mypy nicetree/
```

## Building

Build distribution packages:

```bash
pip install build twine
python -m build
```

## Publishing to PyPI

1. Create account at https://pypi.org/
2. Create `.pypirc` file with credentials
3. Upload:

```bash
python -m twine upload dist/*
```

## Project Structure

```
nicetree/
├── nicetree/              # Main package
│   ├── __init__.py       # Package exports
│   ├── tree.py           # Tree generation
│   ├── formatter.py      # Output formatting
│   └── cli.py            # CLI interface
├── tests/                 # Test suite
│   └── test_nicetree.py
├── docs/                  # Documentation
├── pyproject.toml        # Project metadata
├── setup.py              # Setup script
├── README.md             # User documentation
├── CHANGELOG.md          # Version history
└── LICENSE               # MIT License
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Guidelines

- Write tests for new features
- Update documentation
- Follow code style guidelines
- Update CHANGELOG.md
