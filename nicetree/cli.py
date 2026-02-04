import argparse
import sys
from pathlib import Path
from typing import Optional, List

from nicetree.tree import TreeGenerator
from nicetree.formatter import TreeFormatter, OutputFormat


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nicetree",
        description="Display a directory tree structure in a nice format",
        epilog="Examples:\n"
               "  nicetree                    # Show current directory tree\n"
               "  nicetree /path/to/dir       # Show tree for specific directory\n"
               "  nicetree --depth 2          # Limit tree depth to 2 levels\n"
               "  nicetree --ignore '*.pyc'   # Ignore Python cache files\n"
               "  nicetree --size             # Show file sizes",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the directory to display (default: current directory)"
    )
    
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=None,
        metavar="N",
        help="Limit tree depth to N levels"
    )
    
    parser.add_argument(
        "-i", "--ignore",
        action="append",
        dest="ignore_patterns",
        default=[],
        metavar="PATTERN",
        help="Ignore files matching PATTERN (can be used multiple times)"
    )
    
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Show hidden files (starting with .)"
    )
    
    parser.add_argument(
        "-L", "--follow",
        action="store_true",
        help="Follow symbolic links"
    )
    
    parser.add_argument(
        "-s", "--size",
        action="store_true",
        help="Show file sizes"
    )
    
    parser.add_argument(
        "-S", "--statistics",
        action="store_true",
        help="Show statistics (file/directory counts)"
    )
    
    parser.add_argument(
        "--charset",
        choices=["auto", "unicode", "ascii"],
        default="auto",
        help="Character set to use for drawing (default: auto-detect)"
    )
    
    parser.add_argument(
        "--no-colors",
        action="store_true",
        help="Disable colored output"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["tree", "json", "simple"],
        default="tree",
        help="Output format (default: tree)"
    )
    
    parser.add_argument(
        "-V", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    return parser


def validate_arguments(args: argparse.Namespace) -> None:

    path = Path(args.path)
    
    if not path.exists():
        print(f"Error: Path does not exist: {args.path}", file=sys.stderr)
        sys.exit(1)
    
    if not path.is_dir():
        print(f"Error: Path is not a directory: {args.path}", file=sys.stderr)
        sys.exit(1)
    
    if args.depth is not None and args.depth < 0:
        print("Error: Depth must be non-negative", file=sys.stderr)
        sys.exit(1)


def main(argv: Optional[List[str]] = None) -> int:

    parser = create_parser()
    args = parser.parse_args(argv)
    
    try:
        validate_arguments(args)
        
        generator = TreeGenerator(
            root_path=args.path,
            max_depth=args.depth,
            ignore_patterns=args.ignore_patterns,
            show_hidden=args.all,
            follow_symlinks=args.follow,
            show_size=args.size,
        )
        
        root_node = generator.generate()
        
        if root_node is None:
            print("Error: Could not generate tree", file=sys.stderr)
            return 1
        
        formatter = TreeFormatter(
            charset=args.charset,
            colors=not args.no_colors,
            show_size=args.size,
            format_type=OutputFormat(args.format),
        )
        
        formatter.print_tree(root_node, show_root=True)
        
        if args.statistics:
            stats = generator.get_tree_stats(root_node)
            print("\n" + "=" * 40)
            print(f"Directories: {stats['dir_count']}")
            print(f"Files: {stats['file_count']}")
            if args.size:
                total_mb = stats['total_size'] / (1024 * 1024)
                print(f"Total Size: {total_mb:.2f} MB")
        
        return 0
    
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
