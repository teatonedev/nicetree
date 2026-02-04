#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path


def print_header(text):
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}")


def check_installation():
    print_header("1. Installation Check")
    
    try:
        import nicetree
        print(f" nicetree module imported successfully")
        print(f"   Version: {nicetree.__version__}")
        return True
    except ImportError as e:
        print(f"Failed to import nicetree: {e}")
        return False


def check_components():

    print_header("2. Component Check")
    
    components = {
        "TreeGenerator": "nicetree.tree",
        "TreeFormatter": "nicetree.formatter",
        "TreeNode": "nicetree.tree",
    }
    
    all_ok = True
    for name, module in components.items():
        try:
            exec(f"from {module} import {name}")
            print(f"{name:20} imported")
        except ImportError as e:
            print(f"{name:20} failed: {e}")
            all_ok = False
    
    return all_ok


def check_cli():

    print_header("3. CLI Check")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "nicetree.cli", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"+CLI version check passed")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"-CLI version check failed")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"-CLI check failed: {e}")
        return False


def check_help():

    print_header("4. Help Check")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "nicetree.cli", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and "usage:" in result.stdout.lower():
            print(f"+ Help documentation works")
            lines = result.stdout.count('\n')
            print(f"   Help text: {lines} lines")
            return True
        else:
            print(f"- Help check failed")
            return False
    except Exception as e:
        print(f"- Help check failed: {e}")
        return False


def check_basic_functionality():
    print_header("5. Basic Functionality Check")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "nicetree.cli", ".", "--depth", "1", "--no-colors"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout:
            print(f"+ Tree generation works")
            print(f"   Output lines: {result.stdout.count(chr(10))}")
            print(f"   First line: {result.stdout.split(chr(10))[0][:50]}...")
            return True
        else:
            print(f"- Tree generation failed")
            print(f"   Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"- Functionality check failed: {e}")
        return False


def check_python_api():

    print_header("6. Python API Check")
    
    try:
        from nicetree import TreeGenerator, TreeFormatter
        gen = TreeGenerator(".", max_depth=1)
        root = gen.generate()
        
        if root is None:
            print(f"-Tree generation returned None")
            return False
        
        fmt = TreeFormatter()
        output = fmt.format_tree(root)
        
        if not output:
            print(f"-Tree formatting produced no output")
            return False
        
        print(f"+ Python API works")
        print(f"   Generated tree with {len(output)} characters")
        print(f"   Root node: {root.name}")
        print(f"   Children: {len(root.children)}")
        return True
    
    except Exception as e:
        print(f"- Python API check failed: {e}")
        return False


def check_package_files():

    print_header("7. Package Files Check")
    
    required_files = {
        "pyproject.toml": "Package configuration",
        "README.md": "Documentation",
        "LICENSE": "License file",
        "nicetree/__init__.py": "Package init",
        "nicetree/tree.py": "Tree module",
        "nicetree/formatter.py": "Formatter module",
        "nicetree/cli.py": "CLI module",
        "tests/test_nicetree.py": "Tests",
    }
    
    all_ok = True
    for file_path, description in required_files.items():
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"+ {file_path:35} ({size:,} bytes) - {description}")
        else:
            print(f"- {file_path:35} MISSING - {description}")
            all_ok = False
    
    return all_ok


def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "nicetree - Verification Script" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    
    checks = [
        ("Installation", check_installation),
        ("Components", check_components),
        ("CLI", check_cli),
        ("Help", check_help),
        ("Functionality", check_basic_functionality),
        ("Python API", check_python_api),
        ("Package Files", check_package_files),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"- {name} check failed with exception: {e}")
            results.append((name, False))
    

    print_header("Verification Summary")    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "+ PASS" if result else "- FAIL"
        print(f"{status}  {name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n" + "=" * 60)
        print("++ All checks passed! nicetree is ready to use!")
        print("=" * 60)
        print("\nQuick start:")
        print("  nicetree                    # Show current directory")
        print("  nicetree . -d 2             # Limit to 2 levels")
        print("  nicetree --help             # Show all options")
        print()
        return 0
    else:
        print("\n" + "=" * 60)
        print(f"-!-  {total - passed} check(s) failed. Please review above.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
