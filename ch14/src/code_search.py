"""Code Search Tool with Concurrent Analysis.

This module provides tools for searching and analyzing Python source files
concurrently. It scans directories for Python files, parses their import
statements using the AST (Abstract Syntax Tree), and reports which modules
are imported by each file.

The tool uses ThreadPoolExecutor for concurrent file analysis, making it
efficient for scanning large codebases. Results are highlighted when specific
modules of interest (e.g., 'typing') are imported.

Key Features:
    - Concurrent file analysis using thread pools
    - AST-based import extraction
    - Configurable directory scanning with pattern matching
    - Automatic skipping of common non-source directories
    - Performance metrics reporting

Example Usage:
    # Scan current directory
    python code_search.py

    # Scan specific directories
    python code_search.py /path/to/project1 /path/to/project2

    # Use as a module
    from code_search import main
    main(Path('/path/to/project'))
"""

import argparse
import ast
from concurrent import futures
from fnmatch import fnmatch
import os
from pathlib import Path
import sys
import time
from typing import Iterator, NamedTuple


class ImportResult(NamedTuple):
    """Container for import analysis results.

    This NamedTuple stores the results of analyzing a single Python file,
    including the file path and the set of modules it imports.

    Attributes:
        path (Path): The file path of the analyzed Python source file.
        imports (set[str]): Set of module names imported in the file.

    Properties:
        focus (bool): Returns True if the file imports specific modules of
            interest (currently checks for 'typing' module).

    Example:
        >>> result = ImportResult(Path('module.py'), {'os', 'sys', 'typing'})
        >>> result.focus
        True
        >>> result.imports
        {'os', 'sys', 'typing'}
    """

    path: Path
    imports: set[str]

    @property
    def focus(self) -> bool:
        """Check if this file imports modules of interest.

        Currently highlights files that import the 'typing' module,
        which is useful for identifying files using type annotations.

        Returns:
            bool: True if 'typing' module is imported, False otherwise.
        """
        return "typing" in self.imports


class ImportVisitor(ast.NodeVisitor):
    """AST visitor for extracting import statements from Python code.

    This visitor traverses the Abstract Syntax Tree (AST) of a Python file
    and collects all imported module names, including both regular imports
    (import x) and from-imports (from x import y).

    The visitor pattern is used to walk through AST nodes and process
    specific node types (Import and ImportFrom nodes).

    Attributes:
        imports (set[str]): Accumulated set of module names found in the file.

    Example:
        >>> tree = ast.parse('import os\nfrom pathlib import Path')
        >>> visitor = ImportVisitor()
        >>> visitor.visit(tree)
        >>> visitor.imports
        {'os', 'pathlib'}
    """

    def __init__(self) -> None:
        """Initialize the visitor with an empty imports set."""
        self.imports: set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        """Visit an import statement node (e.g., 'import os').

        Extracts module names from regular import statements and adds them
        to the imports set. Handles multiple imports in a single statement
        (e.g., 'import os, sys').

        Args:
            node (ast.Import): The import statement AST node to process.

        Example:
            Processes: import os, sys, pathlib
            Adds: 'os', 'sys', 'pathlib' to self.imports
        """
        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit a from-import statement node (e.g., 'from os import path').

        Extracts the module name from 'from x import y' statements and adds
        it to the imports set. Only the source module (x) is recorded, not
        the imported names (y).

        Args:
            node (ast.ImportFrom): The from-import statement AST node to process.

        Example:
            Processes: from pathlib import Path, PurePath
            Adds: 'pathlib' to self.imports

        Note:
            Skips relative imports without a module name (e.g., 'from . import x')
        """
