"""
Singleton Design Pattern Examples

This module demonstrates the Singleton design pattern through practical examples:
1. Database Connection Manager
2. Application Logger
3. Configuration Manager
4. Cache Manager

The Singleton pattern ensures that a class has only one instance and provides
a global point of access to that instance. This is useful when you need to
coordinate actions across a system from a single point.

Key Characteristics:
    - Only one instance can exist
    - Global access point to the instance
    - Lazy initialization (created when first needed)
    - Thread-safe implementation considerations

When to Use:
    - Database connection pools
    - Logging systems
    - Configuration managers
    - Caching systems
    - Hardware interface access
    - GUI application instances
"""

import threading
import time
from typing import Optional, Dict, Any


# =============================================================================
# Basic Singleton Implementation
# =============================================================================


class BasicSingleton:
    """
    Basic Singleton implementation using __new__ method.

    This is the simplest way to implement Singleton in Python.
    Uses the __new__ method to control instance creation.
    """

    _instance: Optional["BasicSingleton"] = None

    def __new__(cls):
        """
        Control instance creation to ensure only one instance exists.

        This method is called before __init__ and controls object creation.
        If an instance already exists, returns the existing instance.
        Otherwise, creates a new instance and stores it in _instance.
                Returns:
            BasicSingleton: The single instance of this class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the singleton instance only once.

        Uses the 'initialized' attribute to ensure initialization happens
        only for the first creation, preventing re-initialization on
        subsequent calls to the constructor.

        Note:
            This method may be called multiple times (each time someone
            calls BasicSingleton()), but initialization only happens once.
        """
        # Only initialize once
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.data = "Singleton Instance"

    def get_data(self) -> str:
        """
        Retrieve the data stored in the singleton instance.

        Returns:
            str: The data string stored in this singleton instance.

        Example:
            >>> singleton = BasicSingleton()
            >>> data = singleton.get_data()
            >>> print(data)
            Singleton Instance
        """
        return self.data


# =============================================================================
# Thread-Safe Singleton with Decorator
# =============================================================================


def singleton(cls):
    """
    Decorator to make any class a thread-safe singleton.

    This decorator can be applied to any class to make it a singleton.
    Uses a lock to ensure thread safety during instance creation.
    Implements the double-check locking pattern for optimal performance.

    Args:
        cls (type): The class to be made into a singleton.

    Returns:
        function: A function that returns the singleton instance when called.

    Example:
        >>> @singleton
        ... class MyClass:
        ...     def __init__(self):
        ...         self.value = 42
        >>>
        >>> instance1 = MyClass()
        >>> instance2 = MyClass()
        >>> assert instance1 is instance2  # Same instance

    Note:
        This decorator maintains a separate instance for each decorated class,
        so different classes decorated with @singleton will have their own
        unique singleton instances.
    """
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        """
        Get or create the singleton instance for the decorated class.

        Args:
            *args: Positional arguments to pass to class constructor.
            **kwargs: Keyword arguments to pass to class constructor.

        Returns:
            object: The singleton instance of the decorated class.
        """
        if cls not in instances:
            with lock:
                # Double-check locking pattern
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


# =============================================================================
# Example 1: Database Connection Manager
# =============================================================================


@singleton
class DatabaseManager:
    """
    Singleton Database Connection Manager.

    Manages database connections across the application. Ensures only one
    connection pool exists, preventing resource waste and connection conflicts.

    Real-world Benefits:
        - Prevents multiple connection pools
        - Manages limited database connections efficiently
        - Provides consistent database access across application
        - Handles connection pooling and cleanup
    """

    def __init__(self):
        """
        Initialize the database connection manager.

        Sets up the initial connection pool with default parameters.
        Creates a small initial pool that can grow up to max_connections.

        Attributes:
            connections (list): Available database connections ready for use.
            max_connections (int): Maximum number of connections allowed in pool.
            current_connections (int): Total connections created (in use + available).
        """

        self.connections = []
        self.max_connections = 10
        self.current_connections = 0
        self._initialize_pool()

    def _initialize_pool(self):
        """
        Initialize the connection pool with a default number of connections.

        Creates an initial set of database connections to have ready for use.
        This is more efficient than creating connections on-demand as it
        reduces latency for the first few database operations.

        Note:
            This is a private method called during initialization.
            In a real implementation, this would create actual database
            connections using libraries like psycopg2, pymongo, etc.
        """

        print("🔗 Initializing database connection pool...")
        # Simulate creating database connections
        for i in range(3):  # Start with 3 connections
            self.connections.append(f"Connection-{i + 1}")
            self.current_connections += 1
        print(
            f"✅ Database pool initialized with {self.current_connections} connections"
        )

    def get_connection(self) -> Optional[str]:
        """
        Get an available database connection from the pool.

        Attempts to provide a database connection using the following strategy:
        1. If connections are available in pool, return one immediately
        2. If pool is empty but under max limit, create a new connection
        3. If at max limit, return None (connection not available)

        Returns:
            Optional[str]: A database connection identifier if available,
                          None if no connections can be provided.

        Example:
            >>> db_manager = DatabaseManager()
            >>> conn = db_manager.get_connection()
            >>> if conn:
            ...     # Use connection for database operations
            ...     db_manager.return_connection(conn)

        Note:
            In a real implementation, this would return actual connection
            objects (e.g., psycopg2.connection, sqlite3.Connection).
        """

        if self.connections:
            connection = self.connections.pop(0)
            print(f"📤 Providing connection: {connection}")
            return connection
        elif self.current_connections < self.max_connections:
            # Create new connection if under limit
            self.current_connections += 1
            connection = f"Connection-{self.current_connections}"
            print(f"🆕 Created new connection: {connection}")
            return connection
        else:
            print("⚠️ No connections available!")
            return None

    def return_connection(self, connection: str):
        """
        Return a database connection to the pool for reuse.

        Adds the connection back to the available pool so it can be
        reused by other parts of the application. This is essential
        for efficient resource management in database connection pooling.

        Args:
            connection (str): The connection identifier to return to the pool.

        Example:
            >>> db_manager = DatabaseManager()
            >>> conn = db_manager.get_connection()
            >>> # ... use connection ...
            >>> db_manager.return_connection(conn)  # Return for reuse

        Note:
            In a real implementation, you would also handle connection
            validation (checking if connection is still alive) before
            returning it to the pool.
        """

        self.connections.append(connection)
        print(f"📥 Connection returned to pool: {connection}")

    def get_stats(self) -> Dict[str, int]:
        """
        Get connection pool statistics for monitoring and debugging.

        Provides information about the current state of the connection pool,
        useful for monitoring application performance and debugging
        connection-related issues.

        Returns:
            Dict[str, int]: Dictionary containing pool statistics:
                - 'available': Number of connections ready for use
                - 'total': Total number of connections created
                - 'max': Maximum allowed connections in the pool

        Example:
            >>> db_manager = DatabaseManager()
            >>> stats = db_manager.get_stats()
            >>> print(f"Available connections: {stats['available']}")
            >>> print(f"Pool utilization: {stats['total']}/{stats['max']}")
        """

        return {
            "available": len(self.connections),
            "total": self.current_connections,
            "max": self.max_connections,
        }


# =============================================================================
# Example 4: Cache Manager
# =============================================================================


@singleton
class CacheManager:
    """
    Singleton Cache Manager.

    Manages application-wide caching. Ensures single cache instance to
    prevent memory duplication and provides consistent cache behavior
    across all application modules.

    Real-world Benefits:
        - Prevents multiple cache instances
        - Consistent cache behavior across modules
        - Memory efficiency (no duplicate cached data)
        - Centralized cache invalidation
    """

    def __init__(self):
        """
        Initialize the cache manager with default settings.

        Sets up an empty cache with performance tracking metrics
        and configurable size limits for memory management.

        Attributes:
            cache (dict): The main cache storage for key-value pairs.
            hit_count (int): Number of successful cache retrievals.
            miss_count (int): Number of failed cache retrievals.
            max_size (int): Maximum number of items allowed in cache.
        """

        self.cache = {}
        self.hit_count = 0
        self.miss_count = 0
        self.max_size = 100
        print("💾 Cache manager initialized")

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache by key.

        Attempts to find and return the cached value for the given key.
        Automatically tracks cache performance metrics (hits/misses).

        Args:
            key (str): The cache key to look up.

        Returns:
            Optional[Any]: The cached value if found, None if not in cache.
                          For complex cached objects, returns the nested 'value'.

        Example:
            >>> cache = CacheManager()
            >>> cache.set("user:123", {"name": "Alice", "role": "admin"})
            >>> user_data = cache.get("user:123")
            >>> if user_data:
            ...     print(f"User: {user_data['value']['name']}")

        Note:
            This method does not handle TTL expiration in the current
            implementation but tracks access patterns for monitoring.
        """

        if key in self.cache:
            self.hit_count += 1
            print(f"🎯 Cache HIT: {key}")
            return self.cache[key]
        else:
            self.miss_count += 1
            print(f"❌ Cache MISS: {key}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a value in cache."""
        if len(self.cache) >= self.max_size:
            # Simple LRU: remove first item
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            print(f"🗑️ Evicted oldest cache entry: {oldest_key}")

        self.cache[key] = {"value": value, "timestamp": time.time(), "ttl": ttl}
        print(f"💾 Cached: {key}")

    def delete(self, key: str):
        """Delete a value from cache."""
        if key in self.cache:
            del self.cache[key]
            print(f"🗑️ Deleted from cache: {key}")
            return True
        return False

    def clear(self):
        """Clear all cached data."""
        self.cache.clear()
        print("🧹 Cache cleared")
