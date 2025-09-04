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

    conn.commit()
    return conn


class QueryTemplate:
    """
    Abstract base class implementing the Template Method pattern for database queries.

    This class provides a framework for executing database queries and outputting
    results in CSV format. It defines the overall algorithm structure while allowing
    subclasses to customize specific steps like query construction and output handling.

    The template method process_format() orchestrates the following steps:
    1. Connect to database
    2. Construct query (abstract - must be implemented by subclasses)
    3. Execute query
    4. Output results with proper context management

    Attributes:
        db_name (str): Name of the database file
        conn (sqlite3.Connection): Database connection object
        results (list[tuple[str, ...]]): Query results as list of tuples
        query (str): SQL query string to execute
        header (list[str]): Column headers for CSV output
        target_file (TextIO): Output destination for results

    Abstract Methods:
        construct_query(): Must be implemented to set self.query and self.header

    Template Method:
        process_format(): Orchestrates the complete query processing workflow

    Example:
        >>> class MyQuery(QueryTemplate):
        ...     def construct_query(self):
        ...         self.query = "SELECT * FROM Sales"
        ...         self.header = ["salesperson", "amt", "year", "model", "new"]
        >>>
        >>> query = MyQuery()
        >>> query.process_format()  # Executes complete workflow
    """

    def __init__(self, db_name: str = "sales.db") -> None:
        """
        Initialize the query template with database configuration.

        Args:
            db_name (str, optional): Name of the database file to connect to.
                Defaults to "sales.db".

        Note:
            Connection is not established until connect() is called.
        """

        self.db_name = db_name
        self.conn: sqlite3.Connection
        self.results: list[tuple[str, ...]]
        self.query: str
        self.header: list[str]

    def connect(self) -> None:
        """
        Establish connection to the SQLite database.

        Creates a connection to the database specified in db_name.
        This method is called automatically by process_format().

        Raises:
            sqlite3.Error: If database connection fails.
        """
        self.conn = sqlite3.connect(self.db_name)

    def construct_query(self) -> None:
        """
        Abstract method to construct the SQL query and headers.

        Subclasses must implement this method to:
        - Set self.query to the SQL query string
        - Set self.header to the list of column headers for output

        Raises:
            NotImplementedError: Always, as this is an abstract method.

        Example Implementation:
            >>> def construct_query(self):
            ...     self.query = "SELECT salesperson, amt FROM Sales"
            ...     self.header = ["Salesperson", "Amount"]
        """
        raise NotImplementedError("construct_+query not implemented")

    def do_query(self) -> None:
        """
        Execute the constructed query and fetch all results.

        Runs the SQL query stored in self.query and stores all results
        in self.results as a list of tuples. This method is called
        automatically by process_format().

        Requires:
            - self.conn must be established (via connect())
            - self.query must be set (via construct_query())

        Note:
            Results are fetched entirely into memory using fetchall().
        """
        results = self.conn.execute(self.query)
        self.results = results.fetchall()

    def output_context(self) -> ContextManager[TextIO]:
        """
        Provide context manager for output destination.

        Default implementation outputs to stdout using a null context.
        Subclasses can override this to provide file-based output or
        other output destinations.

        Returns:
            ContextManager[TextIO]: Context manager for output operations.

        Example Override:
            >>> def output_context(self):
            ...     self.target_file = open("output.csv", "w")
            ...     return self.target_file
        """
        self.target_file = sys.stdout
        return cast(ContextManager[TextIO], contextlib.nullcontext())

    def output_results(self) -> None:
        """
        Write query results to the target output in CSV format.

        Uses Python's csv.writer to format results with headers.
        The output destination is determined by the output_context() method.
        This method is called automatically by process_format().

        Requires:
            - self.target_file must be set (via output_context())
            - self.header must contain column headers
            - self.results must contain query results
        """
        writer = csv.writer(self.target_file)
        writer.writerow(self.header)
        writer.writerows(self.results)

    def process_format(self) -> None:
        """
        Template method that orchestrates the complete query processing workflow.

        This is the main method that coordinates all steps:
        1. Connect to database
        2. Construct query (delegated to subclass)
        3. Execute query and fetch results
        4. Output results with proper context management

        This method implements the Template Method pattern, providing
        a fixed algorithm structure while allowing customization of
        specific steps through method overriding.

        Example:
            >>> query = NewVehiclesQuery()
            >>> query.process_format()  # Complete workflow execution
        """
        self.connect()
        self.construct_query()
        self.do_query()
        with self.output_context():
            self.output_results()


class NewVehiclesQuery(QueryTemplate):
    """
    Query implementation for filtering new vehicle sales.

    This class extends QueryTemplate to provide a specific query that filters
    the Sales table to show only new vehicle sales (where new = 'true').
    The results are output to stdout in CSV format.

    Inherits:
        QueryTemplate: Base template for database query operations

    Query Details:
        - Filters Sales table for new vehicles only
        - Returns all columns for matching records
        - Headers: ["salesperson", "amt", "year", "model", "new"]

    Example:
        >>> # Set up database with sample data
        >>> test_setup()
        >>>
        >>> # Query and display new vehicle sales
        >>> query = NewVehiclesQuery()
        >>> query.process_format()
        salesperson,amt,year,model,new
        Tim,16000,2010,Honda Fit,true
        Hannah,28000,2009,Ford Mustang,true
        Hannah,50000,2010,Lincoln Navigator,true
    """

    def construct_query(self) -> None:
        """
        Construct SQL query to filter new vehicle sales.

        Sets up the query to select all columns from Sales table where
        the 'new' column equals 'true', showing only new vehicle sales.

        Sets:
            self.query: SQL SELECT statement with WHERE clause
            self.header: Column headers for CSV output
        """
        self.query = """
            SELECT * FROM Sales WHERE new = 'true'
        """
        self.header = ["salesperson", "amt", "year", "model", "new"]


class SalesGrossQuery(QueryTemplate):
    """
    Query implementation for calculating gross sales by salesperson.

    This class extends QueryTemplate to provide aggregated sales data,
    grouping by salesperson and summing their total sales amounts.
    Results are output to a dated CSV file rather than stdout.

    Inherits:
        QueryTemplate: Base template for database query operations

    Query Details:
        - Groups Sales records by salesperson
        - Calculates sum of sales amounts per person
        - Headers: ["salesperson", "total sales"]
        - Output: CSV file named "gross_sales_YYYYMMDD.csv"

    File Output:
        The output_context() method creates a file with today's date
        in the format "gross_sales_YYYYMMDD.csv" for the results.

    Example:
        >>> # Set up database with sample data
        >>> test_setup()
        >>>
        >>> # Generate gross sales report to file
        >>> query = SalesGrossQuery()
        >>> query.process_format()
        >>> # Creates file: gross_sales_20250903.csv (example date)
        >>>
        >>> # File contents would be:
        >>> # salesperson,total sales
        >>> # Hannah,86000
        >>> # Jason,20000
        >>> # Tim,25000
    """

    def construct_query(self):
        """
        Construct SQL query to calculate gross sales by salesperson.

        Sets up an aggregated query that groups sales records by salesperson
        and calculates the sum of sales amounts for each person.

        Sets:
            self.query: SQL SELECT with GROUP BY and SUM aggregate
            self.header: Column headers for CSV output
        """
        self.query = """
            SELECT salesperson, sum(amt) FROM Sales GROUP BY salesperson
        """
        self.header = ["salesperson", "total sales"]

    def output_context(self) -> ContextManager[TextIO]:
        """
        Create file context for dated CSV output.

        Creates a CSV file with today's date in the filename format
        "gross_sales_YYYYMMDD.csv" for storing the aggregated sales results.

        Returns:
            ContextManager[TextIO]: File context manager for the dated CSV file.

        File Format:
            - Filename: gross_sales_YYYYMMDD.csv (where YYYYMMDD is today's date)
            - Content: CSV format with headers and sales data

        Example:
            If run on September 3, 2025, creates "gross_sales_20250903.csv"
        """
        today = datetime.date.today()
        filepath = Path(f"gross_sales_{today:%Y%m%d}.csv")
        self.target_file = filepath.open("w")
        return self.target_file


def main() -> None:
    """
    Main function to demonstrate car sales analysis workflow.

    Orchestrates the complete sales analysis process:
    1. Sets up database with sample sales data
    2. Runs new vehicles query (output to stdout)
    3. Runs gross sales query (output to dated CSV file)

    This function demonstrates both types of query implementations:
    - NewVehiclesQuery: Filters data and displays to console
    - SalesGrossQuery: Aggregates data and saves to file

    Output Files:
        - gross_sales_YYYYMMDD.csv: Created in current directory

    Console Output:
        - New vehicle sales data in CSV format

    Example:
        >>> main()
        salesperson,amt,year,model,new
        Tim,16000,2010,Honda Fit,true
        Hannah,28000,2009,Ford Mustang,true
        Hannah,50000,2010,Lincoln Navigator,true
        # Also creates gross_sales_20250903.csv file
    """

    test_setup()

    task_1 = NewVehiclesQuery()
    task_1.process_format()

    task_2 = SalesGrossQuery()
    task_2.process_format()
