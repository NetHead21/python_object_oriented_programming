"""
Abstract Factory Pattern - Comprehensive Examples and Implementation Guide

This module provides extensive examples of the Abstract Factory design pattern,
demonstrating its application across multiple domains including GUI frameworks,
infrastructure components, and manufacturing systems.

PATTERN OVERVIEW:
================
The Abstract Factory Pattern is a creational design pattern that provides an
interface for creating families of related or dependent objects without
specifying their concrete classes. It's particularly useful when:

- Your system needs to work with multiple product families
- Products within a family must be compatible with each other
- You want to switch between different product families easily
- You need to ensure consistency across related objects

PATTERN STRUCTURE:
==================
- Abstract Factory: Interface declaring creation methods for abstract products
- Concrete Factory: Implements creation methods for specific product families
- Abstract Product: Interface for a type of product object
- Concrete Product: Specific implementations created by concrete factories
- Client: Uses only abstract factory and product interfaces

EXAMPLES INCLUDED:
==================
1. GUI Components: Cross-platform user interface elements
   - Windows, Mac, and Linux implementations
   - Button, Window, and Menu families
   - Demonstrates platform-specific styling and behavior

2. Infrastructure Components: Environment-specific system components
   - Production, Staging, and Development environments
   - Database, Cache, and Logger families
   - Shows environment-appropriate implementations

3. Vehicle Manufacturing: Different vehicle types and components
   - Luxury, Economy, and Electric vehicle families
   - Engine, Transmission, and Interior components
   - Illustrates manufacturing consistency within product lines

KEY BENEFITS DEMONSTRATED:
==========================
✅ Family Consistency: All products from one factory work together
✅ Easy Switching: Change entire product family with one line
✅ Extensibility: Add new families without changing existing code
✅ Testability: Mock factories enable comprehensive testing
✅ Platform Independence: Client code works across all implementations
✅ SOLID Principles: Follows Open/Closed and Dependency Inversion

USAGE PATTERNS:
===============
1. Factory Selection: Use enums or configuration to choose factories
2. Dependency Injection: Inject factories for flexibility and testing
3. Environment Detection: Automatically select appropriate factory
4. Plugin Architecture: Load factories dynamically for extensibility

Real-world analogies:
- Restaurant chains (McDonald's vs Burger King - different "factories"
  creating compatible families of food items)
- Car manufacturers (BMW vs Toyota - each creates families of compatible
  parts and components)
- Operating systems (Windows vs Mac vs Linux - each provides families
  of compatible UI components and system services)
"""

from abc import ABC, abstractmethod
from typing import List
from enum import Enum


# =============================================================================
# Example 1: GUI Components (Cross-Platform UI)
# =============================================================================


class Button(ABC):
    """Abstract product interface for UI buttons across different platforms.

    This class defines the common interface that all platform-specific buttons
    must implement. It's part of the Abstract Factory pattern where different
    GUI factories create platform-appropriate button implementations.

    The Button interface ensures all concrete buttons provide consistent
    functionality while allowing platform-specific visual styling and behavior.

    Examples:
        WindowsButton implements Windows-style button with system look
        MacButton implements macOS-style button with native appearance
        LinuxButton implements theme-based button following desktop environment
    """

    @abstractmethod
    def render(self) -> str:
        """Render the button with platform-specific styling.

        This method handles the visual representation of the button,
        applying appropriate styling, colors, fonts, and visual effects
        that match the target platform's design guidelines.

        Returns:
            str: Description of the rendered button appearance

        Examples:
            Windows: "Rendering Windows button with rounded corners and gradient"
            Mac: "Rendering Mac button with subtle shadow and system font"
            Linux: "Rendering Linux button with flat design and theme colors"
        """
        pass

    @abstractmethod
    def click(self) -> str:
        """Handle button click events with platform-specific behavior.

        This method processes user clicks on the button, providing
        appropriate feedback (visual, audio, haptic) that matches
        the platform's user experience expectations.

        Returns:
            str: Description of the click interaction and feedback

        Examples:
            Windows: "Windows button clicked with system sound"
            Mac: "Mac button clicked with gentle haptic feedback"
            Linux: "Linux button clicked with configurable action"
        """
        pass


class Window(ABC):
    """Abstract product interface for application windows across different platforms.

    This class defines the common interface for creating and managing application
    windows. Each platform implements this interface to provide native window
    behavior that follows the operating system's window management conventions.

    Windows created through this interface will have platform-appropriate:
    - Title bars and decorations
    - Resize and minimize/maximize controls
    - Close button behavior and animations
    - Focus and z-order management

    Examples:
        WindowsWindow: Native Windows window with Aero styling
        MacWindow: macOS window with traffic light buttons
        LinuxWindow: Desktop environment themed window
    """

    @abstractmethod
    def render(self) -> str:
        """Render the window with platform-specific decorations and styling.

        Creates the visual representation of the window including title bar,
        borders, control buttons, and any platform-specific decorations.
        The styling follows the target platform's design guidelines and
        integrates properly with the desktop environment.

        Returns:
            str: Description of the rendered window appearance

        Examples:
            Windows: "Rendering Windows window with title bar and minimize/maximize buttons"
            Mac: "Rendering Mac window with unified title bar and traffic lights"
            Linux: "Rendering Linux window with customizable decorations"
        """
        pass

    @abstractmethod
    def close(self) -> str:
        """Handle window close operations with platform-appropriate behavior.

        Manages the window closing process including any confirmation dialogs,
        cleanup operations, and closing animations that match the platform's
        expected user experience.

        Returns:
            str: Description of the close operation and animation

        Examples:
            Windows: "Windows window closing with fade animation"
            Mac: "Mac window closing with smooth scale animation"
            Linux: "Linux window closing with user-defined animation"
        """
        pass


class Menu(ABC):
    """Abstract product interface for application menus across different platforms.

    This class defines the common interface for creating platform-specific menu
    systems. Each platform implements menus with their own visual style,
    interaction patterns, and accessibility features while maintaining
    consistent functionality.

    Menu implementations handle:
    - Platform-appropriate styling and theming
    - Keyboard shortcuts and mnemonics
    - Dropdown/popup behavior and animations
    - Menu item highlighting and selection feedback
    - Accessibility features (screen readers, high contrast)

    Examples:
        WindowsMenu: Windows-style menu with drop shadows and system colors
        MacMenu: macOS menu with translucent background and spring animations
        LinuxMenu: Theme-based menu following desktop environment guidelines
    """

    @abstractmethod
    def render(self) -> str:
        """Render the menu with platform-specific styling and layout.

        Creates the visual representation of the menu system including
        styling, colors, fonts, shadows, and visual effects that match
        the target platform's design language and accessibility requirements.

        Returns:
            str: Description of the rendered menu appearance

        Examples:
            Windows: "Rendering Windows menu with drop shadows and hover effects"
            Mac: "Rendering Mac menu with translucent background"
            Linux: "Rendering Linux menu with theme-based styling"
        """
        pass

    @abstractmethod
    def select_item(self, item: str) -> str:
        """Handle menu item selection with platform-specific feedback.

        Processes menu item selection including visual feedback, animations,
        keyboard shortcuts, and any platform-specific interaction patterns.

        Args:
            item (str): The name or identifier of the selected menu item

        Returns:
            str: Description of the selection interaction and feedback

        Examples:
            Windows: "Windows menu item 'File' selected with highlight animation"
            Mac: "Mac menu item 'File' selected with spring animation"
            Linux: "Linux menu item 'File' selected with custom transition"
        """
        pass


# Concrete Products - Windows Style
class WindowsButton(Button):
    """Concrete implementation of Button for Windows platform.

    This class implements the Button interface specifically for Windows,
    providing native Windows look and feel including:
    - Windows Fluent Design styling
    - Rounded corners and gradient backgrounds
    - Windows system sounds for interactions
    - Proper focus indicators and accessibility support
    - Integration with Windows themes and high contrast modes

    The button follows Microsoft's design guidelines for consistency
    with other Windows applications and system components.
    """

    def render(self) -> str:
        """Render a Windows-style button with native styling.

        Creates a button that follows Windows Fluent Design principles
        with appropriate colors, shadows, and visual effects that match
        the current Windows theme and accessibility settings.

        Returns:
            str: Description of the Windows button rendering process
        """
        return "Rendering Windows button with rounded corners and gradient"

    def click(self) -> str:
        """Handle Windows button click with system integration.

        Processes the button click with Windows-appropriate feedback
        including system sounds, visual effects, and proper event handling
        that integrates with Windows accessibility and user preferences.

        Returns:
            str: Description of the Windows click interaction
        """
        return "Windows button clicked with system sound"


class WindowsWindow(Window):
    """Concrete implementation of Window for Windows platform.

    This class implements the Window interface specifically for Windows,
    providing authentic Windows window management including:
    - Windows Aero/Fluent Design window decorations
    - Standard Windows title bar with system buttons
    - Proper integration with Windows window manager
    - Support for Windows accessibility features
    - Snap, minimize, maximize, and close behaviors

    The window follows Windows design guidelines and provides the
    familiar user experience expected in Windows applications.
    """

    def render(self) -> str:
        """Render a Windows-style application window.

        Creates a window with Windows-specific decorations including
        title bar, system buttons, and visual styling that matches
        the current Windows theme and user preferences.

        Returns:
            str: Description of the Windows window rendering
        """
        return "Rendering Windows window with title bar and minimize/maximize buttons"

    def close(self) -> str:
        """Handle Windows window close with appropriate animation.

        Closes the window using Windows-style fade animation and
        proper cleanup that integrates with Windows window management.

        Returns:
            str: Description of the Windows window close operation
        """
        return "Windows window closing with fade animation"


class WindowsMenu(Menu):
    """Concrete implementation of Menu for Windows platform.

    This class implements the Menu interface specifically for Windows,
    providing native Windows menu functionality including:
    - Windows-style drop shadows and visual effects
    - Integration with Windows accessibility features
    - Keyboard shortcuts and mnemonic support
    - Proper hover and selection feedback
    - Context menu support and sub-menu handling

    The menu follows Windows design patterns and provides familiar
    interaction behaviors expected by Windows users.
    """

    def render(self) -> str:
        """Render a Windows-style menu system.

        Creates a menu with Windows-specific styling including
        drop shadows, hover effects, and visual treatments that
        match the current Windows theme.

        Returns:
            str: Description of the Windows menu rendering
        """
        return "Rendering Windows menu with drop shadows and hover effects"

    def select_item(self, item: str) -> str:
        return f"Windows menu item '{item}' selected with highlight animation"


# Concrete Products - Mac Style
class MacButton(Button):
    """Concrete product - Mac-style button"""

    def render(self) -> str:
        return "Rendering Mac button with subtle shadow and system font"

    def click(self) -> str:
        return "Mac button clicked with gentle haptic feedback"


class MacWindow(Window):
    """Concrete product - Mac-style window"""

    def render(self) -> str:
        return "Rendering Mac window with unified title bar and traffic lights"

    def close(self) -> str:
        return "Mac window closing with smooth scale animation"


class MacMenu(Menu):
    """Concrete product - Mac-style menu"""

    def render(self) -> str:
        return "Rendering Mac menu with translucent background"

    def select_item(self, item: str) -> str:
        return f"Mac menu item '{item}' selected with spring animation"


# Concrete Products - Linux Style
class LinuxButton(Button):
    """Concrete product - Linux-style button"""

    def render(self) -> str:
        return "Rendering Linux button with flat design and theme colors"

    def click(self) -> str:
        return "Linux button clicked with configurable action"


class LinuxWindow(Window):
    """Concrete product - Linux-style window"""

    def render(self) -> str:
        return "Rendering Linux window with customizable decorations"

    def close(self) -> str:
        return "Linux window closing with user-defined animation"


class LinuxMenu(Menu):
    """Concrete product - Linux-style menu"""

    def render(self) -> str:
        return "Rendering Linux menu with theme-based styling"

    def select_item(self, item: str) -> str:
        return f"Linux menu item '{item}' selected with custom transition"


# Abstract Factory
class GUIFactory(ABC):
    """Abstract factory interface for creating families of GUI components.

    This is the core of the Abstract Factory pattern, defining the interface
    that all concrete GUI factories must implement. It ensures that families
    of related GUI components (Button, Window, Menu) are created together
    and are compatible with each other.

    The factory pattern provides several key benefits:
    - Ensures consistency: All components from one factory match visually
    - Easy switching: Change platforms by changing the factory instance
    - Extensibility: Add new platforms by implementing this interface
    - Testability: Mock factories can be created for testing

    Each concrete factory (Windows, Mac, Linux) implements this interface
    to create platform-appropriate components that work together seamlessly.

    Example:
        >>> factory = WindowsFactory()
        >>> button = factory.create_button()    # WindowsButton
        >>> window = factory.create_window()    # WindowsWindow
        >>> menu = factory.create_menu()        # WindowsMenu
        >>> # All three components have consistent Windows styling
    """

    @abstractmethod
    def create_button(self) -> Button:
        """Create a platform-specific button component.

        Factory method that creates a button implementation appropriate
        for the target platform. The returned button will have the correct
        styling, behavior, and integration for the platform.

        Returns:
            Button: A concrete button implementation for this platform

        Examples:
            WindowsFactory returns WindowsButton with Windows styling
            MacFactory returns MacButton with macOS styling
            LinuxFactory returns LinuxButton with desktop theme styling
        """
        pass

    @abstractmethod
    def create_window(self) -> Window:
        """Create a platform-specific window component.

        Factory method that creates a window implementation with proper
        platform integration including native decorations, controls,
        and behavior patterns.

        Returns:
            Window: A concrete window implementation for this platform

        Examples:
            WindowsFactory returns WindowsWindow with Aero styling
            MacFactory returns MacWindow with traffic light buttons
            LinuxFactory returns LinuxWindow with desktop environment theme
        """
        pass

    @abstractmethod
    def create_menu(self) -> Menu:
        """Create a platform-specific menu component.

        Factory method that creates a menu system that follows the
        platform's menu conventions, styling, and interaction patterns.

        Returns:
            Menu: A concrete menu implementation for this platform

        Examples:
            WindowsFactory returns WindowsMenu with system styling
            MacFactory returns MacMenu with translucent effects
            LinuxFactory returns LinuxMenu with desktop theme integration
        """
        pass


# Concrete Factories
class WindowsFactory(GUIFactory):
    """Concrete factory implementation for creating Windows GUI component families.

    This factory creates a complete family of Windows-styled GUI components
    that work together seamlessly. All components created by this factory
    follow Microsoft's design guidelines and integrate properly with the
    Windows operating system.

    The factory ensures:
    - Visual consistency: All components use Windows Fluent Design
    - Behavioral consistency: Components follow Windows interaction patterns
    - System integration: Components work with Windows accessibility features
    - Theme support: Components respect Windows system themes and settings

    Components created include:
    - WindowsButton: Native Windows button with system styling
    - WindowsWindow: Windows application window with proper decorations
    - WindowsMenu: Windows-style menu with system integration

    Example:
        >>> factory = WindowsFactory()
        >>> button = factory.create_button()
        >>> window = factory.create_window()
        >>> menu = factory.create_menu()
        >>> # All three components have consistent Windows styling
    """

    def create_button(self) -> Button:
        """Create a Windows-specific button component.

        Returns:
            Button: WindowsButton instance with Windows styling and behavior
        """
        return WindowsButton()

    def create_window(self) -> Window:
        """Create a Windows-specific window component.

        Returns:
            Window: WindowsWindow instance with Windows decorations and controls
        """
        return WindowsWindow()

    def create_menu(self) -> Menu:
        """Create a Windows-specific menu component.

        Returns:
            Menu: WindowsMenu instance with Windows styling and behavior
        """
        return WindowsMenu()


class MacFactory(GUIFactory):
    """Concrete factory for Mac GUI components"""

    def create_button(self) -> Button:
        return MacButton()

    def create_window(self) -> Window:
        return MacWindow()

    def create_menu(self) -> Menu:
        return MacMenu()


class LinuxFactory(GUIFactory):
    """Concrete factory for Linux GUI components"""

    def create_button(self) -> Button:
        return LinuxButton()

    def create_window(self) -> Window:
        return LinuxWindow()

    def create_menu(self) -> Menu:
        return LinuxMenu()


# Client Code - Application using the factory
class Application:
    """Client application that uses the Abstract Factory pattern for GUI creation.

    This class demonstrates how client code should interact with the Abstract
    Factory pattern. It depends only on the abstract factory interface and
    product interfaces, making it platform-agnostic and easily testable.

    Key design principles demonstrated:
    - Dependency on abstractions, not concrete classes
    - Platform-agnostic client code
    - Easy switching between different GUI implementations
    - Factory injection for flexibility and testability

    The application doesn't know or care whether it's creating Windows, Mac,
    or Linux components - it just uses the factory interface to create
    compatible components that work together.

    Attributes:
        factory (GUIFactory): The factory used to create GUI components
        components (List): List of created GUI components

    Example:
        >>> # Create Windows application
        >>> windows_app = Application(WindowsFactory())
        >>> windows_app.create_ui()
        >>> windows_app.render_ui()

        >>> # Switch to Mac without changing application code
        >>> mac_app = Application(MacFactory())
        >>> mac_app.create_ui()
        >>> mac_app.render_ui()
    """

    def __init__(self, factory: GUIFactory):
        """Initialize the application with a specific GUI factory.

        Args:
            factory (GUIFactory): The factory to use for creating GUI components.
                                 This determines the platform/style of all components.
        """

        self.factory = factory
        self.components = []

    def create_ui(self):
        """Create the complete user interface using the injected factory.

        Uses the factory to create a complete set of compatible GUI components.
        All components will be from the same platform family, ensuring
        visual consistency and proper interaction behavior.

        Returns:
            List: The created GUI components (Button, Window, Menu)

        Note:
            This method demonstrates how client code stays platform-agnostic
            by depending only on abstract interfaces.
        """

        button = self.factory.create_button()
        window = self.factory.create_window()
        menu = self.factory.create_menu()

        self.components = [button, window, menu]
        return self.components

    def render_ui(self):
        """Render all created UI components with their platform-specific styling.

        Calls the render method on each component, which will execute the
        platform-appropriate rendering logic based on the concrete implementations
        created by the factory.

        Returns:
            List[str]: Descriptions of how each component was rendered

        Example:
            For Windows factory:
            ["Rendering Windows button...", "Rendering Windows window...", "Rendering Windows menu..."]
        """
        results = []
        for component in self.components:
            results.append(component.render())
        return results


# =============================================================================
# Example 2: Database Abstraction Layer
# =============================================================================


class Database(ABC):
    """Abstract product interface for database connections across different systems.

    This class defines the common interface that all database implementations
    must provide, regardless of the underlying database technology. It's part
    of an infrastructure Abstract Factory that creates compatible sets of
    database, caching, and logging components.

    The Database interface abstracts away the specific details of different
    database systems (MySQL, PostgreSQL, SQLite) while providing a consistent
    API for data operations.

    Implementations should handle:
    - Connection establishment and management
    - Query execution with proper error handling
    - Database-specific optimizations
    - Connection pooling and resource management
    - Transaction support where applicable

    Examples:
        MySQL: Production database with connection pooling
        PostgreSQL: Staging database with SSL encryption
        SQLite: Development database with local file storage
    """

    @abstractmethod
    def connect(self) -> str:
        """Establish connection to the database system.

        Handles the connection process including authentication,
        connection string parsing, SSL configuration, and any
        database-specific initialization requirements.

        Returns:
            str: Description of the connection establishment process

        Examples:
            MySQL: "Connected to MySQL database with connection pooling"
            PostgreSQL: "Connected to PostgreSQL with SSL encryption"
            SQLite: "Connected to SQLite local database"
        """
        pass

    @abstractmethod
    def execute_query(self, query: str) -> str:
        """Execute a database query with appropriate optimization and error handling.

        Processes SQL queries using database-specific optimization strategies,
        parameter binding, and error handling appropriate for the database system.

        Args:
            query (str): The SQL query to execute

        Returns:
            str: Description of query execution with database-specific details

        Examples:
            MySQL: "Executing MySQL query: {query} with optimization"
            PostgreSQL: "Executing PostgreSQL query: {query} with ACID compliance"
            SQLite: "Executing SQLite query: {query} on local file"
        """
        pass


class Cache(ABC):
    """Abstract product interface for caching systems across different environments.

    This class defines the common interface for all cache implementations
    in the infrastructure Abstract Factory. Different environments may use
    different caching technologies (Redis, Memcached, in-memory) but all
    must provide consistent get/set operations.

    Cache implementations should handle:
    - Key-value storage and retrieval
    - Expiration and eviction policies
    - Network communication (for distributed caches)
    - Serialization/deserialization of cached data
    - Error handling and fallback behavior

    Examples:
        RedisCache: Distributed cache for production environments
        MemcachedCache: High-performance cache for staging
        InMemoryCache: Simple cache for development and testing
    """

    @abstractmethod
    def get(self, key: str) -> str:
        """Retrieve a value from the cache by its key.

        Args:
            key (str): The cache key to look up

        Returns:
            str: Description of the cache retrieval operation

        Examples:
            Redis: "Retrieved from Redis cache: user_123"
            Memcached: "Retrieved from Memcached: user_123"
            InMemory: "Retrieved from memory cache: user_123"
        """
        pass

    @abstractmethod
    def set(self, key: str, value: str) -> str:
        """Store a value in the cache with the given key.

        Args:
            key (str): The cache key for storage
            value (str): The value to cache

        Returns:
            str: Description of the cache storage operation

        Examples:
            Redis: "Stored in Redis cache: user_123 = user_data"
            Memcached: "Stored in Memcached: user_123 = user_data"
            InMemory: "Stored in memory cache: user_123 = user_data"
        """
        pass


class Logger(ABC):
    """Abstract product interface for logging systems across different environments.

    This class defines the common interface for all logging implementations
    in the infrastructure Abstract Factory. Different environments may
    require different logging approaches (files, syslog, console) but all
    must provide consistent logging capabilities.

    Logger implementations should handle:
    - Message formatting and timestamp handling
    - Log level management and filtering
    - Output destination management
    - Error handling and fallback logging
    - Performance considerations for high-volume logging

    Examples:
        FileLogger: Production logging to rotating files
        SyslogLogger: System logging for staging environments
        ConsoleLogger: Development logging to console output
    """

    @abstractmethod
    def log(self, message: str) -> str:
        """Log a message using the environment-appropriate logging mechanism.

        Args:
            message (str): The message to log

        Returns:
            str: Description of where and how the message was logged

        Examples:
            File: "Logged to file: Application started successfully"
            Syslog: "Logged to syslog: Application started successfully"
            Console: "Console log: Application started successfully"
        """
        pass


# MySQL Infrastructure
class MySQL(Database):
    """MySQL-specific implementation of the Database interface."""

    def connect(self) -> str:
        return "Connected to MySQL database with connection pooling"

    def execute_query(self, query: str) -> str:
        return f"Executing MySQL query: {query} with optimization"


class RedisCache(Cache):
    """Cache impelemention for Redis"""

    def get(self, key: str) -> str:
        return f"Retrieved from Redis cache: {key}"

    def set(self, key: str, value: str) -> str:
        return f"Stored in Redis cache: {key} = {value}"


class FileLogger(Logger):
    def log(self, message: str) -> str:
        return f"Logged to file: {message}"


# PostgreSQL Infrastructure
class PostgreSQL(Database):
    """Postgres-specific implementation of the Database interface."""

    def connect(self) -> str:
        return "Connected to PostgreSQL with SSL encryption"

    def execute_query(self, query: str) -> str:
        return f"Executing PostgreSQL query: {query} with ACID compliance"


class MemcachedCache(Cache):
    """Cache implementation for Memcached"""

    def get(self, key: str) -> str:
        return f"Retrieved from Memcached: {key}"

    def set(self, key: str, value: str) -> str:
        return f"Stored in Memcached: {key} = {value}"


class SyslogLogger(Logger):
    def log(self, message: str) -> str:
        return f"Logged to syslog: {message}"


# SQLite Infrastructure
class SQLite(Database):
    """SQLite-specific implementation of the Database interface."""

    def connect(self) -> str:
        return "Connected to SQLite local database"

    def execute_query(self, query: str) -> str:
        return f"Executing SQLite query: {query} on local file"


class InMemoryCache(Cache):
    """Cache implementation for in-memory caching"""

    def get(self, key: str) -> str:
        return f"Retrieved from memory cache: {key}"


class ConsoleLogger(Logger):
    def log(self, message: str) -> str:
        return f"Console log: {message}"


# Infrastructure Factory
class InfrastructureFactory(ABC):
    """Abstract factory for creating infrastructure components"""

    @abstractmethod
    def create_database(self) -> Database:
        pass

    @abstractmethod
    def create_cache(self) -> Cache:
        pass

    @abstractmethod
    def create_logger(self) -> Logger:
        pass


class ProductionFactory(InfrastructureFactory):
    """Factory for production environment"""

    def create_database(self) -> Database:
        return MySQL()

    def create_cache(self) -> Cache:
        return RedisCache()

    def create_logger(self) -> Logger:
        return FileLogger()


class StagingFactory(InfrastructureFactory):
    """Factory for staging environment"""
