# nice tree

![alt text](docs/nicetree_logo.png)

A robust Python utility that functions like the Unix `tree` command with cross-platform support (macOS, Linux, and Windows). Display directory hierarchies in a beautiful, formatted structure with extensive customization options.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Features

- **Cross-platform support**: Works seamlessly on macOS, Linux, and Windows
- **Beautiful output**: Unicode tree drawing with optional colors
- **Customizable**: Control depth, filtering, and output format
- **Performance**: Efficient directory traversal
- **Symbolic link handling**: Properly handles symlinks with circular reference detection
- **File sizes**: Display file/directory sizes in human-readable format
- **Multiple formats**: Tree, JSON, and simple text output
- **Hidden file control**: Show or hide dot-files
- **Pattern matching**: Ignore files matching patterns (wildcards supported)
- **Statistics**: Display file/directory counts

## Installation

### From PyPI (Recommended)

```bash
pip install nice-tree
```

### From source

```bash
git clone https://github.com/teatonedev/nicetree.git
cd nicetree
pip install -e .
```

### Development installation

```bash
git clone https://github.com/teatonedev/nicetree.git
cd nicetree
pip install -e ".[dev]"
```

## Quick Start

### Command Line Usage

```bash
# Display current directory tree
nicetree

# Display specific directory
nicetree /path/to/directory

# Limit depth to 2 levels
nicetree --depth 2

# Show file sizes
nicetree --size

# Ignore Python cache files
nicetree --ignore "*.pyc" --ignore "__pycache__"

# Show hidden files
nicetree --all

# Show statistics
nicetree --statistics

# Follow symbolic links
nicetree --follow

# Use ASCII characters
nicetree --charset ascii

# Disable colors
nicetree --no-colors

# JSON output
nicetree --format json
```

### Python API Usage

```python
from nicetree import TreeGenerator, TreeFormatter, OutputFormat

# Create generator
generator = TreeGenerator(
    root_path="/path/to/dir",
    max_depth=3,
    show_hidden=False,
    ignore_patterns=["*.pyc", "__pycache__"],
    show_size=True,
)

# Generate tree
root_node = generator.generate()

# Create formatter
formatter = TreeFormatter(
    charset="unicode",
    colors=True,
    show_size=True,
    format_type=OutputFormat.TREE,
)

# Display tree
formatter.print_tree(root_node)

# Or get as string
output = formatter.format_tree(root_node)
print(output)

# Get statistics
stats = generator.get_tree_stats(root_node)
print(f"Files: {stats['file_count']}, Directories: {stats['dir_count']}")
```

## CLI Reference

### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--depth` | `-d` | INT | Limit tree depth to N levels |
| `--ignore` | `-i` | PATTERN | Ignore files matching PATTERN (can be used multiple times) |
| `--all` | `-a` | - | Show hidden files (starting with .) |
| `--follow` | `-L` | - | Follow symbolic links |
| `--size` | `-s` | - | Show file sizes |
| `--statistics` | `-S` | - | Show statistics (file/directory counts) |
| `--charset` | - | {auto,unicode,ascii} | Character set for drawing (default: auto) |
| `--no-colors` | - | - | Disable colored output |
| `--format` | `-f` | {tree,json,simple} | Output format (default: tree) |
| `--version` | `-V` | - | Show version information |

### Examples

```bash
# Display current directory with all options
nicetree . --all --depth 3 --size --statistics

# Export as JSON
nicetree /var/log --format json > tree.json

# Show only Python files (2 levels deep)
nicetree . --depth 2 --ignore "*.pyc" --ignore "*.pyo"

# ASCII output for piping to other commands
nicetree --charset ascii --no-colors

# Show large directories
nicetree /home --depth 2 --size --statistics
```

## API Reference

### TreeGenerator

Main class for generating directory tree structures.

#### Constructor

```python
TreeGenerator(
    root_path: str = ".",
    max_depth: Optional[int] = None,
    ignore_patterns: Optional[List[str]] = None,
    show_hidden: bool = False,
    follow_symlinks: bool = False,
    show_size: bool = False,
    case_sensitive: bool = True,
)
```

#### Parameters

- **root_path**: Starting directory (default: current directory)
- **max_depth**: Maximum traversal depth (None = unlimited)
- **ignore_patterns**: List of wildcard patterns to ignore
- **show_hidden**: Include hidden files (starting with .)
- **follow_symlinks**: Follow symbolic links (with circular detection)
- **show_size**: Calculate and display file/directory sizes
- **case_sensitive**: Use case-sensitive pattern matching

#### Methods

- `generate() -> Optional[TreeNode]`: Build and return the tree structure
- `get_tree_stats(node: Optional[TreeNode]) -> Dict[str, int]`: Get statistics about the tree

### TreeFormatter

Formats and displays tree structures.

#### Constructor

```python
TreeFormatter(
    charset: str = "auto",
    colors: bool = True,
    show_size: bool = False,
    format_type: OutputFormat = OutputFormat.TREE,
)
```

#### Parameters

- **charset**: "unicode", "ascii", or "auto" (auto-detect)
- **colors**: Use ANSI colors in output
- **show_size**: Display file sizes
- **format_type**: OutputFormat enum (TREE, JSON, or SIMPLE)

#### Methods

- `format_tree(node: Optional[TreeNode], show_root: bool = True) -> str`: Return formatted tree as string
- `print_tree(node: Optional[TreeNode], show_root: bool = True) -> None`: Print tree to stdout

### TreeNode

Represents a single node in the directory tree.

#### Attributes

- **name**: Node name (filename or directory name)
- **path**: Full Path object
- **is_dir**: Boolean indicating if node is a directory
- **is_symlink**: Boolean indicating if node is a symbolic link
- **children**: List of child TreeNode objects
- **size**: File/directory size in bytes

## Platform-Specific Notes

### macOS
- Full Unicode support with automatic color detection
- Symbolic links fully supported
- All features available

### Linux
- Full Unicode support
- Color support depends on TERM variable
- Excellent performance on large directory trees
- All features available

### Windows
- ASCII character set used by default (can override)
- Color support in Windows 10+ with ANSICON
- Path handling automatically converts to Windows format
- Symbolic link support available with appropriate permissions

## Performance

nicetree is optimized for performance:

- **Lazy loading**: Only traverses necessary paths based on options
- **Efficient symlink detection**: Tracks visited inodes to prevent loops
- **Streaming output**: Outputs as it traverses (for large trees)
- **Memory efficient**: Uses generators where possible

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Teatonedev Batt ([abbilginn@hotmail.com](mailto:abbilginn@hotmail.com))

## Changelog

### Version 1.0.0 (2026-01-26)
- Initial release
- Full cross-platform support
- CLI and Python API
- Comprehensive testing
- PyPI distribution ready
