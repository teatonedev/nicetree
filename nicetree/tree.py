import os
import sys
import fnmatch
      
from pathlib import Path
from typing import List, Dict, Optional, Set, Callable
from dataclasses import dataclass, field


@dataclass
class TreeNode:
    name: str
    path: Path
    is_dir: bool
    is_symlink: bool = False
    children: List['TreeNode'] = field(default_factory=list)
    size: int = 0
    
    def __lt__(self, other: 'TreeNode') -> bool:

        if self.is_dir != other.is_dir:
            return self.is_dir
        return self.name.lower() < other.name.lower()


class TreeGenerator:    
    def __init__(
        self,
        root_path: str = ".",
        max_depth: Optional[int] = None,
        ignore_patterns: Optional[List[str]] = None,
        show_hidden: bool = False,
        follow_symlinks: bool = False,
        show_size: bool = False,
        case_sensitive: bool = True,
    ):
        self.root_path = Path(root_path).resolve()
        self.max_depth = max_depth
        self.ignore_patterns = ignore_patterns or []
        self.show_hidden = show_hidden
        self.follow_symlinks = follow_symlinks
        self.show_size = show_size
        self.case_sensitive = case_sensitive
        self.visited_dirs: Set[int] = set()
        
    def _should_ignore(self, name: str, path: Path) -> bool:
      
        if not self.show_hidden and name.startswith('.'):
            return True
        
        for pattern in self.ignore_patterns:
            if self._matches_pattern(name, pattern):
                return True
        
        return False
    
    def _matches_pattern(self, name: str, pattern: str) -> bool:  
        name_to_check = name if self.case_sensitive else name.lower()
        pattern_to_check = pattern if self.case_sensitive else pattern.lower()
        
        return fnmatch.fnmatch(name_to_check, pattern_to_check)
    
    def _is_circular_symlink(self, path: Path) -> bool:
      
        if not path.is_symlink():
            return False
        
        try:
            resolved = path.resolve()
            inode = os.stat(resolved).st_ino
            
            if inode in self.visited_dirs:
                return True
            
            self.visited_dirs.add(inode)
            return False
        except (OSError, RuntimeError):
            return True
    
    def _get_node_size(self, path: Path) -> int:
        try:
            if path.is_file():
                return path.stat().st_size
            elif path.is_dir():
                return sum(
                    f.stat().st_size 
                    for f in path.rglob('*') 
                    if f.is_file()
                )
        except (OSError, PermissionError):
            pass
        return 0
    
    def _build_tree(self, path: Path, depth: int = 0) -> Optional[TreeNode]:
        if self.max_depth is not None and depth > self.max_depth:
            return None
        

        if self._should_ignore(path.name, path):
            return None
        
        try:
            is_symlink = path.is_symlink()
            try:
                is_dir = path.is_dir(follow_symlinks=False)
            except TypeError:
                is_dir = path.is_dir() if not is_symlink else False
            
            if is_symlink:
                if not self.follow_symlinks:
                    return TreeNode(
                        name=path.name,
                        path=path,
                        is_dir=False,
                        is_symlink=True,
                        size=0
                    )
                
                if self._is_circular_symlink(path):
                    return TreeNode(
                        name=path.name,
                        path=path,
                        is_dir=False,
                        is_symlink=True,
                        size=0
                    )
            
            node = TreeNode(
                name=path.name,
                path=path,
                is_dir=is_dir,
                is_symlink=is_symlink,
                size=self._get_node_size(path) if self.show_size else 0
            )
            
            if is_dir:
                try:
                    entries = sorted(path.iterdir())
                except PermissionError:
                    return node
                
                for entry in entries:
                    child_node = self._build_tree(entry, depth + 1)
                    if child_node:
                        node.children.append(child_node)
                
                node.children.sort()
            
            return node
        
        except (OSError, PermissionError):
            return None
    
    def generate(self) -> Optional[TreeNode]:
        if not self.root_path.exists():
            raise ValueError(f"Path does not exist: {self.root_path}")
        
        self.visited_dirs.clear()
        return self._build_tree(self.root_path)
    
    def get_tree_stats(self, node: Optional[TreeNode] = None) -> Dict[str, int]:
        if node is None:
            node = self.generate()
        
        if node is None:
            return {"file_count": 0, "dir_count": 0, "total_size": 0}
        
        stats = {"file_count": 0, "dir_count": 0, "total_size": 0}
        
        def traverse(n: TreeNode):
            if n.is_dir:
                stats["dir_count"] += 1
            else:
                stats["file_count"] += 1
            
            stats["total_size"] += n.size
            
            for child in n.children:
                traverse(child)
        
        traverse(node)
        return stats
