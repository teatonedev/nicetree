# nicetree - Quick Reference

## Installation

```bash
# Current development version
cd /Users/uhem-batuhan/Projects/nicetree
pip install -e .

# Once published to PyPI
pip install nicetree
```

## Basic Commands

```bash
# Current directory
nicetree

# Specific directory
nicetree /path/to/dir

# Help
nicetree --help

# Version
nicetree --version
```

## Common Options

```bash
# Depth limiting
nicetree -d 2                          # 2 levels deep
nicetree --depth 3

# File filtering
nicetree -i "*.pyc"                   # Ignore pattern
nicetree -i "*.pyc" -i "__pycache__"  # Multiple patterns

# Hidden files
nicetree -a                           # Show all (hidden)
nicetree --all

# File sizes
nicetree -s                           # With sizes
nicetree --size

# Statistics
nicetree -S                           # Show counts
nicetree --statistics

# Symbolic links
nicetree -L                           # Follow links
nicetree --follow

# Output format
nicetree -f json                      # JSON output
nicetree -f tree                      # Tree format (default)
nicetree -f simple                    # Simple text

# Character set
nicetree --charset unicode            # Unicode chars
nicetree --charset ascii              # ASCII chars
nicetree --charset auto               # Auto-detect (default)

# Colors
nicetree --no-colors                  # Disable colors
```

## Practical Examples

```bash
# Project structure without cache
nicetree . -d 3 -i "*.pyc" -i "__pycache__" -i ".git"

# Python project overview
nicetree . -d 2 -i "node_modules" -i ".git" -i "__pycache__"

# Show everything
nicetree . -a -d 3 -s -S

# Export to file
nicetree . > structure.txt

# JSON export
nicetree . -f json > structure.json

# Pipe to grep
nicetree . --no-colors | grep "\.py$"

# Large directory analysis
nicetree /home -d 2 -s -S

# Windows directory
nicetree C:\Users\username --charset ascii
```

## Python API Quick Start

```python
# Import
from nicetree import TreeGenerator, TreeFormatter

# Generate
gen = TreeGenerator(".", max_depth=2)
root = gen.generate()

# Format and print
fmt = TreeFormatter()
fmt.print_tree(root)

# Get statistics
stats = gen.get_tree_stats(root)
print(f"Files: {stats['file_count']}, Dirs: {stats['dir_count']}")
```

## Advanced API Usage

```python
from nicetree.tree import TreeGenerator, TreeNode
from nicetree.formatter import TreeFormatter, OutputFormat

# With options
gen = TreeGenerator(
    root_path=".",
    max_depth=3,
    ignore_patterns=["*.pyc", "__pycache__"],
    show_hidden=False,
    follow_symlinks=True,
    show_size=True,
)

root = gen.generate()

# Different formats
tree_fmt = TreeFormatter(format_type=OutputFormat.TREE)
json_fmt = TreeFormatter(format_type=OutputFormat.JSON)

# Get outputs
tree_output = tree_fmt.format_tree(root)
json_output = json_fmt.format_tree(root)
```

## Testing

```bash
# Run all tests
cd /Users/uhem-batuhan/Projects/nicetree
python3 -m pytest tests/test_nicetree.py -v

# Run specific test
python3 -m pytest tests/test_nicetree.py::TestTreeGenerator -v

# With coverage
python3 -m pytest tests/ --cov=nicetree --cov-report=html
```

## Development

```bash
# Install in dev mode
pip install -e ".[dev]"

# Code style
black nicetree/ tests/        # Format
flake8 nicetree/ tests/       # Lint
mypy nicetree/                # Type check

# Build package
python3 -m build

# Check distribution
twine check dist/*
```

## Distribution

```bash
# Build
python3 -m build

# List files in wheel
unzip -l dist/nicetree-1.0.0-py3-none-any.whl

# Extract tar
tar -tzf dist/nicetree-1.0.0.tar.gz

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Troubleshooting

```bash
# Check installation
pip show nicetree

# Run as module
python3 -m nicetree.cli .

# Debug mode
python3 -c "from nicetree import TreeGenerator; g = TreeGenerator('.'); print(g.generate())"

# Version check
python3 -c "import nicetree; print(nicetree.__version__)"
```

## Project Structure Reference

```
nicetree/
├── nicetree/               # Main package
│   ├── tree.py            # TreeGenerator, TreeNode
│   ├── formatter.py       # TreeFormatter, OutputFormat
│   ├── cli.py             # Command-line interface
│   └── __init__.py        # Package exports
├── tests/
│   └── test_nicetree.py  # All 14 tests (passing ✅)
├── docs/                  # Documentation
├── dist/                  # Built packages
├── pyproject.toml        # Modern config
├── README.md             # Main docs
└── LICENSE               # MIT
```

## Documentation Files

| File | Purpose |
|------|---------|
| README.md | Main documentation and API reference |
| docs/GETTING_STARTED.md | Quick start (5 minutes) |
| docs/USAGE.md | Detailed usage examples |
| docs/DEVELOPMENT.md | Development setup |
| docs/PUBLISHING.md | PyPI publishing guide |
| PROJECT_SUMMARY.md | Project overview |
| COMPLETION_CHECKLIST.md | Feature checklist |

## Key Features

- Cross-platform (Windows, macOS, Linux)
- Beautiful tree output with colors
- Multiple output formats (tree, JSON, text)
- File filtering and depth limiting
- No external dependencies
- Comprehensive documentation
- Full test coverage
- Production-ready

## Support

- **Issues**: Check docs/ folder first
- **Questions**: See README.md and docs/USAGE.md
- **Contributing**: See docs/DEVELOPMENT.md

---

**nicetree v1.0.0** - Cross-platform tree command utility
