# nicetree - Getting Started

Welcome to nicetree! This document will help you get started quickly.

## What is nicetree?

nicetree is a python utility that displays directory hierarchies in a beautiful, tree format - similar to the Unix `tree` command. It works on Windows, macOS, and Linux with extensive customization options. I did this because I could not find a good alternative that works under/with pip python.

## Quick Start (5 minutes)

### Step 1: Install

```bash
pip install nicetree
```

### Step 2: Run

```bash
# Show current directory
nicetree

# Show a specific directory
nicetree /path/to/directory

# With options
nicetree . --depth 2 --size
```

### Step 3: Explore

```bash
# Show help
nicetree --help

# Try different options
nicetree . --all              # Show hidden files
nicetree . --size             # Show file sizes
nicetree . --statistics       # Show counts
nicetree . --format json      # JSON output
```

That's it! You're now using nicetree.

## Common Use Cases

### View Project Structure

```bash
cd my_project
nicetree . -d 2 --ignore "node_modules" --ignore ".git"
```

### Clean Code Analysis

```bash
# Show Python files and structure
nicetree . -i "*.pyc" -i "__pycache__" -i ".git" -d 3
```

### Documentation

```bash
# Export directory structure as text
nicetree . --charset ascii --no-colors > structure.txt

# Export as JSON for processing
nicetree . --format json > structure.json
```

### System Administration

```bash
# Audit directory sizes
nicetree /home/users --depth 2 --size --statistics

# Find large directories
nicetree /var/log --size --statistics
```

## Python API

If you're a developer, use nicetree in your python code as:

```python
from nicetree import TreeGenerator, TreeFormatter

# Generate tree
generator = TreeGenerator(".", max_depth=2)
root = generator.generate()

# Display it
formatter = TreeFormatter()
formatter.print_tree(root)
```

## Installation Verification

```bash
# Verify installation
python3 -c "import nicetree; print(nicetree.__version__)"

# Should output: 1.0.0
```

## Troubleshooting

### Command Not Found

If `nicetree` command doesn't work:

```bash
# Check installation
pip show nicetree

# Run as module
python3 -m nicetree.cli .
```

### Permission Issues

```bash
# Install for current user
pip install --user nicetree
```

### Terminal Issues

```bash
nicetree . --charset ascii --no-colors
```

## Next Steps

1. **Read the full documentation**: See [docs/USAGE.md](USAGE.md)
2. **Check the API**: See [README.md](../README.md) for full API reference
3. **View examples**: See [docs/USAGE.md](USAGE.md) for detailed examples
4. **Contribute**: See [docs/DEVELOPMENT.md](DEVELOPMENT.md) if interested in contributing

## Key Features

- + **Cross-platform**: Works on Windows, macOS, and Linux
- + **Beautiful output**: Unicode tree drawing with colors
- + **Flexible**: Control depth, filtering, and format
- + **Fast**: Optimized for performance
- + **Robust**: Handles symlinks and edge cases
- + **Programmable**: Use as Python library

## Support

- **Bug reports**: https://github.com/teatonedev/nicetree/issues
- **Documentation**: See docs/ folder
- **Questions**: Check README.md and docs/USAGE.md

## License

MIT - See LICENSE file for details

---

Happy tree browsing!
