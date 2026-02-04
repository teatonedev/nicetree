# Installation and Usage Guide

Complete guide for installing and using nicetree.

## Installation

### Method 1: pip (Recommended)

```bash
pip install nicetree
```

### Method 2: From Source

```bash
git clone https://github.com/teatonedev/nicetree.git
cd nicetree
pip install -e .
```

### Method 3: Development Installation

For contributors:

```bash
git clone https://github.com/teatonedev/nicetree.git
cd nicetree
pip install -e ".[dev]"
pip install pytest pytest-cov black flake8 mypy
```

## Platform-Specific Notes

### macOS

```bash
# Homebrew (if added as formula)
brew install nicetree

# Or via pip
pip install nicetree
```

### Linux (Debian/Ubuntu)

```bash
# Via pip (recommended)
pip install nicetree

```

### Windows

```bash
# Via pip
pip install nicetree

# Command line support (use with WSL or PowerShell)
nicetree C:\path\to\directory
```

## Basic Usage

### Command Line

Display the current directory:
```bash
nicetree
```

Display a specific directory:
```bash
nicetree /path/to/directory
```

### Common Options

```bash
# Limit depth to 2 levels
nicetree . -d 2

# Show hidden files
nicetree . -a

# Show file sizes
nicetree . -s

# Show statistics
nicetree . -S

# Ignore patterns
nicetree . -i "*.pyc" -i "__pycache__"

# ASCII output (for terminal compatibility)
nicetree . --charset ascii

# Disable colors
nicetree . --no-colors

# JSON output
nicetree . -f json
```

### Combined Examples

```bash
# Show project structure without Python cache
nicetree . -d 3 -i "*.pyc" -i "__pycache__" -i ".git"

# Show everything with sizes and stats
nicetree /home/user -a -s -S

# Export as JSON for processing
nicetree . -f json > tree.json

# ASCII tree for terminal compatibility
nicetree . --charset ascii --no-colors
```

## Python API

### Basic Usage

```python
from nicetree import TreeGenerator, TreeFormatter

# Generate tree
generator = TreeGenerator("/path/to/dir", max_depth=3)
root = generator.generate()

# Format and print
formatter = TreeFormatter()
formatter.print_tree(root)
```

### Advanced Usage

```python
from nicetree.tree import TreeGenerator, TreeNode
from nicetree.formatter import TreeFormatter, OutputFormat

# Create generator with options
generator = TreeGenerator(
    root_path="/path/to/dir",
    max_depth=4,
    ignore_patterns=["*.pyc", "__pycache__", ".git"],
    show_hidden=False,
    follow_symlinks=False,
    show_size=True,
    case_sensitive=False,
)

# Generate tree
root_node = generator.generate()
if root_node is None:
    print("Error generating tree")
    exit(1)

# Get statistics
stats = generator.get_tree_stats(root_node)
print(f"Directories: {stats['dir_count']}")
print(f"Files: {stats['file_count']}")
print(f"Total size: {stats['total_size']} bytes")

# Format as different types
tree_formatter = TreeFormatter(
    charset="unicode",
    colors=True,
    show_size=True,
    format_type=OutputFormat.TREE,
)

# Print to console
tree_formatter.print_tree(root_node)

# Get as string
output = tree_formatter.format_tree(root_node)
print(output)

# JSON format
json_formatter = TreeFormatter(format_type=OutputFormat.JSON)
json_output = json_formatter.format_tree(root_node)
print(json_output)
```

### Working with TreeNode

```python
from nicetree.tree import TreeGenerator

generator = TreeGenerator(".")
root = generator.generate()

def print_tree_recursive(node, indent=0):
    """Recursively print tree structure"""
    prefix = "  " * indent
    node_type = "📁" if node.is_dir else "📄"
    size_str = f" ({node.size} bytes)" if node.size else ""
    print(f"{prefix}{node_type} {node.name}{size_str}")
    
    for child in node.children:
        print_tree_recursive(child, indent + 1)

print_tree_recursive(root)
```

### Filtering Examples

```python
# Filter files by extension
def filter_python_files(generator, root):
    """Keep only Python files"""
    def traverse(node):
        if not node.is_dir:
            if not node.name.endswith('.py'):
                return False
        
        node.children = [
            child for child in node.children 
            if traverse(child)
        ]
        return True
    
    traverse(root)
    return root

# Filter large files
def filter_by_size(generator, root, max_size=1024*1024):
    """Keep only files smaller than max_size"""
    def traverse(node):
        if not node.is_dir and node.size > max_size:
            return False
        
        node.children = [
            child for child in node.children 
            if traverse(child)
        ]
        return True
    
    traverse(root)
    return root
```

## Integration Examples

### Integrate with Other Tools

```bash
# Pipe to grep for searching
nicetree . --no-colors | grep "\.py"

# Count files
nicetree . --no-colors | wc -l

# Export to file
nicetree . > directory_tree.txt

# JSON processing with jq
nicetree . -f json | jq '.children[].name'
```

### Using in Scripts

```python
#!/usr/bin/env python3

import sys
from pathlib import Path
from nicetree.tree import TreeGenerator
from nicetree.formatter import TreeFormatter, OutputFormat

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    try:
        generator = TreeGenerator(target_dir, max_depth=3, show_size=True)
        root = generator.generate()
        
        if root:
            formatter = TreeFormatter(show_size=True)
            formatter.print_tree(root)
            
            stats = generator.get_tree_stats(root)
            print(f"\nTotal: {stats['file_count']} files, {stats['dir_count']} directories")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Troubleshooting

### Command Not Found

If `nicetree` command is not found:

```bash
# Check if installed
pip list | grep nicetree

# If installed but not found, add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or run as module
python3 -m nicetree.cli
```

### Permission Denied

If getting permission errors:

```bash
# Run with sudo (not recommended)
sudo nicetree /root

# Or install with appropriate permissions
pip install --user nicetree
```

### Special Characters in Output

For terminal compatibility issues:

```bash
# Use ASCII mode
nicetree . --charset ascii

# Disable colors
nicetree . --no-colors

# Both
nicetree . --charset ascii --no-colors
```

### Large Directory Performance

For very large directories:

```bash
# Limit depth
nicetree /very/large/dir -d 2

# Use patterns to exclude
nicetree /very/large/dir -i "node_modules" -i ".git"
```

## Tips and Tricks

### Aliases

Add to your shell config (~/.bashrc, ~/.zshrc, etc.):

```bash
# Simple alias
alias tree="nicetree"

# With common options
alias tree2="nicetree -d 2 --no-colors"
alias treea="nicetree -a -d 3"  # Show all, 3 levels
```

### Compare Directory Structures

```bash
# Create trees
nicetree ~/projects/old-project > tree_old.txt
nicetree ~/projects/new-project > tree_new.txt

# Compare
diff tree_old.txt tree_new.txt
```

### Regular Expressions with Ignore Patterns

```bash
# Ignore multiple extensions
nicetree . -i "*.pyc" -i "*.pyo" -i "*.pyd"

# Exclude directories
nicetree . -i "node_modules" -i "__pycache__" -i ".git"
```

## Getting Help

```bash
# Show help
nicetree --help

# Show version
nicetree --version

# Check documentation
python3 -c "from nicetree import TreeGenerator; help(TreeGenerator)"
```
