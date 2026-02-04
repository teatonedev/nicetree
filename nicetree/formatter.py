import sys

from pathlib import Path
from typing import Optional, List, Callable
from enum import Enum
from nicetree.tree import TreeNode


class OutputFormat(Enum):
    TREE = "tree"
    JSON = "json"
    SIMPLE = "simple"


class TreeFormatter:    
    CONNECTOR = "├── "
    LAST_CONNECTOR = "└── "
    PIPE = "│   "
    BLANK = "    "
    
    def __init__(
        self,
        charset: str = "auto",
        colors: bool = True,
        show_size: bool = False,
        format_type: OutputFormat = OutputFormat.TREE,
    ):
        self.show_size = show_size
        self.format_type = format_type
        self.colors = colors and self._supports_colors()
        
        self._set_charset(charset)
    
    def _supports_colors(self) -> bool:
      
        if not sys.stdout.isatty():
            return False
        
        term = os.environ.get('TERM', '').lower()
        if term == 'dumb':
            return False
        
        if sys.platform == 'win32':
            return sys.version_info >= (3, 10) or 'ANSICON' in os.environ
        
        return True
    
    def _set_charset(self, charset: str) -> None:
      
        if charset == "auto":
            use_unicode = sys.platform != "win32"
        else:
            use_unicode = charset == "unicode"
        
        if use_unicode:
            self.CONNECTOR = "├── "
            self.LAST_CONNECTOR = "└── "
            self.PIPE = "│   "
            self.BLANK = "    "
        else:
            self.CONNECTOR = "+-- "
            self.LAST_CONNECTOR = "\\-- "
            self.PIPE = "|   "
            self.BLANK = "    "
    
    def _get_color_code(self, color_type: str) -> str:
      
        if not self.colors:
            return ""
        
        colors = {
            "dir": "\033[34m",
            "symlink": "\033[36m",
            "reset": "\033[0m",
            "bold": "\033[1m",
            "gray": "\033[90m",
        }
        return colors.get(color_type, "")
    
    def _format_size(self, size: int) -> str:
      
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"
    
    def _format_node_name(self, node: TreeNode) -> str:
      
        name = node.name
        
        if node.is_dir and not name.endswith('/'):
            name += "/"
        
        if node.is_symlink:
            name += " -> "
            try:
                target = Path(node.path).resolve()
                name += str(target)
            except Exception:
                name += "[circular]"
        
        if self.colors:
            if node.is_symlink:
                name = f"{self._get_color_code('symlink')}{name}{self._get_color_code('reset')}"
            elif node.is_dir:
                name = f"{self._get_color_code('dir')}{name}{self._get_color_code('reset')}"
        
        if self.show_size and node.size > 0:
            size_str = self._format_size(node.size)
            size_str = f" {self._get_color_code('gray')}({size_str}){self._get_color_code('reset')}"
            name += size_str
        
        return name
    
    def format_tree(self, node: Optional[TreeNode], show_root: bool = True) -> str:
        if node is None:
            return ""
        
        if self.format_type == OutputFormat.JSON:
            return self._format_as_json(node)
        
        lines = []
        
        if show_root:
            lines.append(self._format_node_name(node))
        
        if node.children:
            for i, child in enumerate(node.children):
                is_last = i == len(node.children) - 1
                lines.extend(
                    self._format_node_recursive(
                        child, "", is_last
                    )
                )
        
        return "\n".join(lines)
    
    def _format_node_recursive(
        self, 
        node: TreeNode, 
        prefix: str, 
        is_last: bool
    ) -> List[str]:

        lines = []
        
        connector = self.LAST_CONNECTOR if is_last else self.CONNECTOR
        lines.append(prefix + connector + self._format_node_name(node))
        
        if node.children:
            extension = self.BLANK if is_last else self.PIPE
            new_prefix = prefix + extension
            
            for i, child in enumerate(node.children):
                child_is_last = i == len(node.children) - 1
                lines.extend(
                    self._format_node_recursive(child, new_prefix, child_is_last)
                )
        
        return lines
    
    def _format_as_json(self, node: Optional[TreeNode]) -> str:

        import json
        
        def node_to_dict(n: TreeNode) -> dict:
            return {
                "name": n.name,
                "type": "directory" if n.is_dir else "file",
                "symlink": n.is_symlink,
                "size": n.size,
                "children": [node_to_dict(child) for child in n.children],
            }
        
        if node is None:
            return json.dumps({}, indent=2)
        
        return json.dumps(node_to_dict(node), indent=2)
    
    def print_tree(self, node: Optional[TreeNode], show_root: bool = True) -> None:
        output = self.format_tree(node, show_root)
        if output:
            print(output)


import os
