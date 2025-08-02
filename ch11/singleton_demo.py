#!/usr/bin/env python3
"""
Quick Singleton Pattern Demonstration

Shows real-world examples of the Singleton pattern in action.
"""

import threading
from typing import Optional, Dict, Any


# =============================================================================
# 1. Database Manager Example
# =============================================================================


class DatabaseManager:
    """Singleton Database Connection Manager"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.connections = ["conn1", "conn2", "conn3"]
            self.initialized = True
            print("🔗 Database manager initialized")

    def get_connection(self):
        if self.connections:
            conn = self.connections.pop()
            print(f"📤 Provided connection: {conn}")
            return conn
        return None

    def return_connection(self, conn):
        self.connections.append(conn)
        print(f"📥 Returned connection: {conn}")


# =============================================================================
# 2. Logger Example
# =============================================================================


class Logger:
    """Singleton Application Logger"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "logs"):
            self.logs = []
            print("📝 Logger initialized")

    def log(self, message, level="INFO"):
        log_entry = f"[{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)

    def get_log_count(self):
        return len(self.logs)


# =============================================================================
# 3. Configuration Manager Example
# =============================================================================


class ConfigManager:
    """Singleton Configuration Manager"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "config"):
            self.config = {
                "database_url": "localhost:5432",
                "api_key": "secret123",
                "debug_mode": False,
            }
            print("⚙️ Configuration loaded")

    def get(self, key):
        return self.config.get(key)

    def set(self, key, value):
        self.config[key] = value
        print(f"🔧 Config updated: {key} = {value}")


# =============================================================================
# Real-World Demonstrations
# =============================================================================


def demonstrate_database_singleton():
    """Show database manager singleton in action"""
    print("\n" + "=" * 50)
    print("DATABASE MANAGER SINGLETON")
    print("=" * 50)

    # Different parts of app getting database manager
    db1 = DatabaseManager()  # User service
    db2 = DatabaseManager()  # Product service

    print(f"Same instance? {db1 is db2}")  # Should be True

    # Use connections
    conn = db1.get_connection()
    db2.return_connection(conn)


def demonstrate_logger_singleton():
    """Show logger singleton in action"""
    print("\n" + "=" * 50)
    print("LOGGER SINGLETON")
    print("=" * 50)

    # Different modules using logger
    logger1 = Logger()  # Auth module
    logger2 = Logger()  # API module

    print(f"Same logger instance? {logger1 is logger2}")

    # Log from different modules
    logger1.log("User logged in", "INFO")
    logger2.log("API request received", "DEBUG")

    print(f"Total logs: {logger1.get_log_count()}")


def demonstrate_config_singleton():
    """Show configuration manager singleton in action"""
    print("\n" + "=" * 50)
    print("CONFIGURATION MANAGER SINGLETON")
    print("=" * 50)

    # Different services accessing config
    config1 = ConfigManager()  # Database service
    config2 = ConfigManager()  # API service

    print(f"Same config instance? {config1 is config2}")

    # Access config
    print(f"Database URL: {config1.get('database_url')}")
    print(f"Debug mode: {config2.get('debug_mode')}")

    # Update config from one place
    config1.set("debug_mode", True)
    print(f"Debug mode after update: {config2.get('debug_mode')}")


if __name__ == "__main__":
    print("SINGLETON PATTERN REAL-WORLD EXAMPLES")
    print("=" * 60)

    demonstrate_database_singleton()
    demonstrate_logger_singleton()
    demonstrate_config_singleton()

    print("\n" + "=" * 60)
    print("✅ SINGLETON BENEFITS DEMONSTRATED:")
    print("• Single instance across entire application")
    print("• Global access point for shared resources")
    print("• Prevents resource duplication and conflicts")
    print("• Ensures consistent state across modules")
