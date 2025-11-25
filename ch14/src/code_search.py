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
