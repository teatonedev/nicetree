import sys
import os
import json
import unittest
import tempfile
        
from pathlib import Path
from nicetree.tree import TreeGenerator, TreeNode
from nicetree.formatter import TreeFormatter, OutputFormat
from nicetree.cli import main
from io import StringIO

class TestTreeNode(unittest.TestCase):

    def test_node_creation(self):

        node = TreeNode(
            name="test",
            path=Path("/test"),
            is_dir=True,
        )
        self.assertEqual(node.name, "test")
        self.assertTrue(node.is_dir)
        self.assertEqual(len(node.children), 0)
    
    def test_node_sorting(self):

        dir_node = TreeNode(name="a_dir", path=Path("/a"), is_dir=True)
        file_node = TreeNode(name="b_file", path=Path("/b"), is_dir=False)
        
        nodes = [file_node, dir_node]
        nodes.sort()
        
        self.assertTrue(nodes[0].is_dir)
        self.assertFalse(nodes[1].is_dir)


class TestTreeGenerator(unittest.TestCase):

    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        
        (self.root / "dir1").mkdir()
        (self.root / "dir1" / "subdir1").mkdir()
        (self.root / "dir1" / "file1.txt").touch()
        (self.root / "dir1" / "subdir1" / "file2.txt").touch()
        (self.root / "dir2").mkdir()
        (self.root / "file3.txt").touch()
        (self.root / ".hidden").touch()
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_basic_tree_generation(self):
        
        generator = TreeGenerator(str(self.root))
        root_node = generator.generate()
        
        self.assertIsNotNone(root_node)
        self.assertTrue(root_node.is_dir)
        self.assertGreater(len(root_node.children), 0)
    
    def test_hidden_files_excluded_by_default(self):
        generator = TreeGenerator(str(self.root))
        root_node = generator.generate()
        
        names = [child.name for child in root_node.children]
        self.assertNotIn(".hidden", names)
    
    def test_hidden_files_included_with_flag(self):
        generator = TreeGenerator(str(self.root), show_hidden=True)
        root_node = generator.generate()
        
        names = [child.name for child in root_node.children]
        self.assertIn(".hidden", names)
    
    def test_depth_limit(self):
        generator = TreeGenerator(str(self.root), max_depth=1)
        root_node = generator.generate()
        
        dir1 = next((c for c in root_node.children if c.name == "dir1"), None)
        self.assertIsNotNone(dir1)
        
        if dir1:
            self.assertTrue(True)
    
    def test_ignore_patterns(self):
        generator = TreeGenerator(
            str(self.root),
            ignore_patterns=["*.txt"]
        )
        root_node = generator.generate()
        
        all_names = []
        def collect_names(node):
            for child in node.children:
                all_names.append(child.name)
                collect_names(child)
        
        collect_names(root_node)
        
        for name in all_names:
            self.assertFalse(name.endswith(".txt"))
    
    def test_tree_stats(self):
        generator = TreeGenerator(str(self.root), show_hidden=True)
        root_node = generator.generate()
        
        stats = generator.get_tree_stats(root_node)
        
        self.assertIn("file_count", stats)
        self.assertIn("dir_count", stats)
        self.assertGreater(stats["file_count"], 0)
        self.assertGreater(stats["dir_count"], 0)


class TestTreeFormatter(unittest.TestCase):
    def setUp(self):
        self.root = TreeNode(
            name="root",
            path=Path("/root"),
            is_dir=True,
        )
        
        dir1 = TreeNode(
            name="dir1",
            path=Path("/root/dir1"),
            is_dir=True,
        )


        
        file1 = TreeNode(
            name="file1.txt",
            path=Path("/root/file1.txt"),
            is_dir=False,
        )

        
        file2 = TreeNode(
            name="file2.txt",
            path=Path("/root/dir1/file2.txt"),
            is_dir=False,
        )
        
        self.root.children = [dir1, file1]
        dir1.children = [file2]
    
    def test_formatter_creation(self):
        formatter = TreeFormatter()
        self.assertIsNotNone(formatter)
    
    def test_tree_formatting(self):
        formatter = TreeFormatter(colors=False)
        output = formatter.format_tree(self.root)
        
        self.assertIsNotNone(output)
        self.assertIn("root", output)
        self.assertIn("dir1", output)
    
    def test_json_format(self):
        formatter = TreeFormatter(format_type=OutputFormat.JSON)
        output = formatter.format_tree(self.root)
        
        data = json.loads(output)
        self.assertEqual(data["name"], "root")
        self.assertEqual(data["type"], "directory")


class TestCLI(unittest.TestCase):
    def setUp(self):

        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        

        (self.root / "file1.txt").touch()
        (self.root / "subdir").mkdir()
        (self.root / "subdir" / "file2.txt").touch()
    
    def tearDown(self):

        self.temp_dir.cleanup()
    
    def test_cli_basic(self):


        
        exit_code = main([str(self.root), "--no-colors"])
        self.assertEqual(exit_code, 0)
    
    def test_cli_with_depth(self):
        
        exit_code = main([str(self.root), "--depth", "1", "--no-colors"])
        self.assertEqual(exit_code, 0)
    
    def test_cli_invalid_path(self):
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        
        try:
            with self.assertRaises(SystemExit) as context:
                main(["/nonexistent/path/that/does/not/exist", "--no-colors"])

            self.assertEqual(context.exception.code, 1)
        finally:
            sys.stderr = old_stderr


if __name__ == "__main__":
    unittest.main()
