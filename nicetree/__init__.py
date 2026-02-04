"""
nicetree: A cross-platform Python utility that functions like the tree Linux command.

This module provides the core functionality for displaying directory trees in a
structured format with customizable options for filtering, depth limiting, and output.
"""

__version__ = "1.0.0"
__author__ = "teatonedev"
__license__ = "MIT"

from nicetree.tree import TreeGenerator
from nicetree.formatter import TreeFormatter

__all__ = ["TreeGenerator", "TreeFormatter", "__version__"]
