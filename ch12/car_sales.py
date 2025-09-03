"""
Car Sales Data Analysis Module

This module provides functionality for analyzing car sales data using SQLite database
operations and CSV output generation. It demonstrates the Template Method design pattern
for database query processing and supports various types of sales analysis reports.

The module contains:
    - Database setup and initialization with sample data
    - QueryTemplate: Abstract base class implementing the Template Method pattern
    - NewVehiclesQuery: Query for filtering new vehicle sales
    - SalesGrossQuery: Query for calculating gross sales by salesperson
    - CSV output generation with flexible destination handling

Key Features:
    • Template Method pattern for consistent query processing workflow
    • SQLite database integration with automatic schema creation
    • Flexible output handling (stdout or file-based CSV generation)
    • Date-based filename generation for reports
    • Comprehensive sales data analysis capabilities

Example Usage:
    >>> # Set up database and run analysis
    >>> test_setup()
    >>>
    >>> # Generate new vehicles report to stdout
    >>> new_vehicles = NewVehiclesQuery()
    >>> new_vehicles.process_format()
    >>>
    >>> # Generate gross sales report to dated CSV file
    >>> gross_sales = SalesGrossQuery()
    >>> gross_sales.process_format()

Dependencies:
    - contextlib: For context manager operations
    - csv: For CSV file generation
    - pathlib: For file path operations
    - sqlite3: For database operations
    - typing: For type hints
    - sys: For stdout access
    - datetime: For date-based file naming
"""

import contextlib
import csv
import datetime
from pathlib import Path
import sqlite3
from typing import ContextManager, TextIO, cast
import sys


def test_setup(db_name: str = "sales.db") -> sqlite3.Connection:
    """
    Set up and initialize the sales database with sample data.

    Creates a SQLite database with a Sales table and populates it with
    sample car sales data for testing and demonstration purposes. The
    function handles table creation, data cleanup, and sample data insertion.

    Args:
        db_name (str, optional): Name of the database file to create/use.
            Defaults to "sales.db".

    Returns:
        sqlite3.Connection: Connected database object ready for queries.

    Database Schema:
        Sales table with columns:
        - salesperson (text): Name of the salesperson
        - amt (currency): Sale amount in currency units
        - year (integer): Year of the vehicle
        - model (text): Vehicle model name
        - new (boolean): Whether the vehicle is new ('true'/'false')

    Sample Data:
        - Tim: Honda Fit 2010 (new, $16,000), Ford Focus 2006 (used, $9,000)
        - Hannah: Dodge Neon 2004 (used, $8,000), Ford Mustang 2009 (new, $28,000),
                  Lincoln Navigator 2010 (new, $50,000)
        - Jason: Toyota Prius 2008 (used, $20,000)

    Example:
        >>> conn = test_setup()
        >>> cursor = conn.execute("SELECT COUNT(*) FROM Sales")
        >>> print(cursor.fetchone()[0])  # Should print 6
        6
        >>> conn.close()

        >>> # Use custom database name
        >>> conn = test_setup("my_sales.db")
        >>> conn.close()
    """

    conn = sqlite3.connect(db_name)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Sales(
            salesperson text,
            amt currency,
            year integer,
            model text,
            new boolean
            );
        """
    )

    conn.execute(
        """
        DELETE FROM Sales
        """
    )

    conn.execute(
        """
        INSERT INTO Sales 
        VALUES('Tim', 16000, 2010, 'Honda Fit', 'true')
        """
    )
    conn.execute(
        """
        INSERT INTO Sales 
        VALUES('Tim', 9000, 2006, 'Ford Focus', 'false')
        """
    )

    conn.execute(
        """
        INSERT INTO Sales 
        VALUES('Hannah', 8000, 2004, 'Dodge Neon', 'false')
        """
    )
    conn.execute(
        """
        INSERT INTO Sales 
        VALUES('Hannah', 28000, 2009, 'Ford Mustang', 'true')
        """
    )
    conn.execute(
        """
        INSERT INTO Sales 
        VALUES('Hannah', 50000, 2010, 'Lincoln Navigator', 'true')
        """
    )
    conn.execute(
        """
        INSERT INTO Sales 
        VALUES('Jason', 20000, 2008, 'Toyota Prius', 'false')
        """
    )
