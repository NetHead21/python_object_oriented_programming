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
