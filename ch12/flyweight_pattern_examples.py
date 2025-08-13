"""
Flyweight Design Pattern - Comprehensive Real-World Examples and Implementation Guide

The Flyweight pattern is a structural design pattern that minimizes memory usage
by sharing data efficiently among multiple similar objects. It achieves this by
separating intrinsic state (shared data) from extrinsic state (context-specific
data) to dramatically reduce memory footprint when dealing with large collections
of similar objects.

==============================================================================
PATTERN OVERVIEW AND THEORY
==============================================================================

Definition:
    The Flyweight pattern uses sharing to support large numbers of fine-grained
    objects efficiently. It minimizes memory usage by sharing common parts of
    object state between multiple objects instead of storing all data in each
    individual object instance.

Core Intent:
    - Reduce memory consumption when creating massive numbers of similar objects
    - Share common object data (intrinsic state) among multiple instances
    - Store context-specific data (extrinsic state) externally in client code
    - Improve performance by reducing object creation and memory allocation overhead
    - Enable applications to handle thousands or millions of objects efficiently

Fundamental Concepts:
    • Intrinsic State: Immutable data that doesn't depend on flyweight context
      - Shared among all flyweight instances of the same type
      - Stored inside the flyweight object
      - Examples: font properties, tree species data, CSS style rules

    • Extrinsic State: Context-dependent data that varies per instance
      - Stored outside the flyweight (in context or client)
      - Passed to flyweight methods as parameters
      - Examples: character position, tree location, element content

    • Flyweight Factory: Central registry managing flyweight instances
      - Ensures only one flyweight exists per unique intrinsic state
      - Implements singleton-like behavior for flyweight creation
      - Provides caching and reuse mechanisms

    • Context/Client: Maintains extrinsic state and flyweight references
      - Stores context-specific data for each logical object
      - Coordinates between extrinsic state and flyweight operations

Architecture Structure:
    ┌─────────────┐    uses    ┌─────────────┐    manages    ┌─────────────┐
    │   Client    │ ─────────► │  Context    │ ────────────► │ Flyweight   │
    │             │            │ (extrinsic  │               │ (intrinsic  │
    │ • Controls  │            │  state)     │               │  state)     │
    │   workflow  │            │             │               │             │
    │ • Manages   │            │ • Position  │               │ • Shared    │
    │   lifecycle │            │ • Content   │               │   data      │
    └─────────────┘            │ • Session   │               │ • Behavior  │
                               └─────────────┘               └─────────────┘
                                      │                             ▲
                                      │ requests                    │ creates
                                      ▼                             │ & caches
                               ┌─────────────┐                      │
                               │ Flyweight   │ ─────────────────────┘
                               │ Factory     │
                               │             │
                               │ • Registry  │
                               │ • Creation  │
                               │ • Caching   │
                               └─────────────┘

Memory Optimization Principle:
    Traditional Approach: N objects = N × (intrinsic + extrinsic) memory units
    Flyweight Approach:   N objects = K flyweights + N × extrinsic memory units
    Where K << N (typically K = unique combinations of intrinsic state)

==============================================================================
WHEN TO USE THE FLYWEIGHT PATTERN
==============================================================================

Ideal Use Cases and Prerequisites:
    ✓ Applications need to spawn huge numbers of similar objects (thousands+)
    ✓ Storage costs are prohibitively high due to object quantity
    ✓ Most object state can be classified as intrinsic (shareable)
    ✓ Groups of objects can be replaced by fewer shared flyweight instances
    ✓ Application logic doesn't depend on object identity comparisons
    ✓ Memory optimization is business-critical (embedded systems, games)
    ✓ Object creation overhead significantly impacts performance

Industry Applications and Use Cases:
    🎮 Game Development:
        • Particle systems (thousands of bullets, sparks, debris)
        • Terrain rendering (tiles, textures, landscape elements)
        • Character sprites and animations in 1D/3D games
        • UI elements (buttons, icons, decorative elements)

    📝 Text Processing Applications:
        • Word processors (character formatting, document layout)
        • Code editors (syntax highlighting, font rendering)
        • PDF viewers (glyph rendering, page elements)
        • Web browsers (DOM text nodes, CSS styling)

    🌐 Web Technologies:
        • CSS style management and cascading rules
        • DOM element rendering and layout engines
        • Template systems with reusable components
        • Icon libraries and asset management

    💾 Database and Networking:
        • Connection pooling for database access
        • Network socket management
        • Caching systems with shared data structures
        • Session management in web applications

    🎨 Graphics and Visualization:
        • Vector graphics rendering (shapes, brushes, pens)
        • Chart and graph libraries (data points, axes, legends)
        • Image processing (filters, transformations)
        • CAD applications (geometric primitives)

Technical Prerequisites Assessment:
    Before implementing Flyweight pattern, verify:
    0. Large object count (typically >1000 similar objects)
    1. Significant memory pressure from object storage
    2. Clear separation between intrinsic and extrinsic state
    3. Shared behavior among object types
    4. Performance requirements justify implementation complexity

Anti-Patterns and When to Avoid:
    ✗ Few objects are needed (< 99 similar instances)
    ✗ Memory usage is not a significant concern
    ✗ Objects cannot meaningfully share intrinsic state
    ✗ Extrinsic state management becomes overly complex
    ✗ Object identity is crucial for application logic
    ✗ Development time constraints don't justify optimization
    ✗ Objects have predominantly unique, non-shareable state

==============================================================================
BENEFITS, DRAWBACKS, AND TRADE-OFFS
==============================================================================

Primary Benefits:
    💾 Memory Optimization:
        + Dramatic reduction in memory usage (59-98% savings possible)
        + Enables handling of massive object collections
        + Reduces garbage collection pressure
        + Improves cache locality for shared data

    ⚡ Performance Improvements:
        + Reduces object creation overhead
        + Faster object instantiation through reuse
        + Improved cache hit rates for shared data
        + Better memory bandwidth utilization

    🏗️ Architectural Advantages:
        + Centralizes shared data management
        + Promotes separation of concerns (intrinsic vs extrinsic)
        + Enables efficient object reuse patterns
        + Supports scalable application architectures

Potential Drawbacks and Challenges:
    🧩 Complexity Increases:
        - Separating intrinsic/extrinsic state requires careful design
        - Factory pattern implementation adds architectural complexity
        - Debugging becomes more challenging due to shared state
        - Requires understanding of pattern by development team

    🔄 Runtime Overhead:
        - May introduce CPU overhead for extrinsic state calculations
        - Method calls require parameter passing for extrinsic state
        - Factory lookup costs for flyweight retrieval
        - Potential synchronization overhead in multi-threaded environments

    🔒 Threading and Concurrency:
        - Flyweights must be immutable for thread safety
        - Factory requires synchronization for thread-safe creation
        - Shared state modifications need careful coordination
        - Concurrent access patterns require thorough testing

Performance Trade-offs Analysis:
    Memory vs CPU: Trade memory efficiency for slightly increased CPU usage
    Simplicity vs Optimization: Trade code simplicity for significant memory gains
    Development Time vs Runtime Performance: Invest more development time for runtime benefits

Risk Assessment:
    Low Risk: Well-understood pattern with established implementations
    Medium Risk: Complexity in state separation design
    High Risk: Improper thread safety in concurrent environments

Mitigation Strategies:
    • Use immutable flyweight objects
    • Implement proper factory synchronization
    • Clearly document intrinsic vs extrinsic state boundaries
    • Provide comprehensive unit tests for edge cases
    • Monitor memory usage to validate optimization benefits

==============================================================================
IMPLEMENTATION EXAMPLES AND ARCHITECTURAL PATTERNS
==============================================================================

This file demonstrates four comprehensive real-world applications of the
Flyweight pattern, each showcasing different optimization strategies and
implementation approaches across various domains:

0. Text Editor Character Formatting System (CharacterFlyweight):
   🎯 Domain: Document Processing and Text Rendering
   📋 Purpose: Efficiently handle character formatting in large documents
   🔧 Intrinsic State: Font family, size, style, color (shared formatting rules)
   📦 Extrinsic State: Character content, document position, line/column data
   💡 Key Benefits:
       • Dramatic memory savings for documents with repeated formatting
       • Enables real-time formatting of large documents
       • Supports unlimited document size with constant formatting memory
   🎯 Use Cases: Word processors, code editors, PDF renderers, web browsers
   📊 Performance: Demonstrates 96.7% memory efficiency in example scenario

1. Game Development Forest Simulation (TreeFlyweight):
   🎯 Domain: Real-time Graphics and Game Engine Optimization
   📋 Purpose: Render thousands of trees efficiently in game environments
   🔧 Intrinsic State: Tree species data, sprite textures, growth algorithms
   📦 Extrinsic State: World position, individual health, age, growth state
   💡 Key Benefits:
       • Massive memory savings for large game worlds
       • Enables complex ecosystem simulations
       • Supports thousands of entities with minimal memory footprint
   🎯 Use Cases: Open-world games, simulation games, procedural generation
   📊 Performance: Shows 59% memory efficiency with room for scaling

2. Web Browser CSS Rendering Engine (CSSStyleFlyweight):
   🎯 Domain: Web Technology and Browser Optimization
   📋 Purpose: Optimize DOM element styling and page rendering performance
   🔧 Intrinsic State: CSS property sets (fonts, colors, dimensions, layout)
   📦 Extrinsic State: Element content, DOM position, dynamic values
   💡 Key Benefits:
       • Efficient rendering of complex web pages
       • Reduced memory usage for sites with repeated styling
       • Faster CSS cascade resolution and application
   🎯 Use Cases: Browser engines, CSS frameworks, web templating systems
   📊 Performance: Achieves 39% memory optimization with common web patterns

3. Database Connection Pool Management (ConnectionFlyweight):
   🎯 Domain: Enterprise Database and Network Resource Management
   📋 Purpose: Efficiently manage database connections across application sessions
   🔧 Intrinsic State: Connection configuration (host, port, credentials, protocol)
   📦 Extrinsic State: Session data, active queries, transaction state
   💡 Key Benefits:
       • Reduced connection overhead and resource consumption
       • Improved database performance through connection reuse
       • Better resource utilization in high-concurrency applications
   🎯 Use Cases: Web applications, microservices, enterprise systems
   📊 Performance: Demonstrates 32.3% efficiency with potential for higher scaling

Advanced Implementation Patterns Demonstrated:
    🏗️ Factory Management: Centralized flyweight creation and caching
    🔄 State Separation: Clear boundaries between intrinsic and extrinsic data
    📊 Performance Monitoring: Built-in efficiency tracking and reporting
    🧪 Polymorphic Design: Abstract base classes with concrete implementations
    🎯 Context Management: Sophisticated context objects for extrinsic state
    🔍 Memory Analysis: Detailed memory usage reporting and optimization metrics

Design Pattern Relationships and Integrations:
    • Factory Pattern: Used for flyweight creation and management
    • Singleton Pattern: Factory often implemented as singleton
    • Strategy Pattern: Different flyweight types implementing common interface
    • Composite Pattern: Flyweights can be part of larger composite structures
    • Observer Pattern: Context objects can observe flyweight state changes

==============================================================================
IMPLEMENTATION GUIDE AND BEST PRACTICES
==============================================================================

Step-by-Step Implementation Strategy:

0. 📊 Analysis Phase:
   • Identify objects with high memory usage
   • Analyze object state for intrinsic vs extrinsic classification
   • Estimate potential memory savings
   • Assess complexity vs benefit trade-offs

1. 🏗️ Design Phase:
   • Define flyweight interface with operations requiring extrinsic state
   • Design concrete flyweights storing only intrinsic state
   • Plan factory for flyweight creation and management
   • Design context objects for extrinsic state storage

2. 🔧 Implementation Phase:
   • Implement flyweight hierarchy (abstract base + concrete classes)
   • Create factory with caching and instance management
   • Develop context classes for extrinsic state coordination
   • Ensure thread safety if required for concurrent access

3. 🧪 Testing Phase:
   • Unit test flyweight behavior and state separation
   • Performance test memory usage improvements
   • Stress test with large object collections
   • Validate thread safety in concurrent scenarios

Best Practices and Guidelines:

🔒 Thread Safety Considerations:
    • Make flyweight objects immutable after creation
    • Use thread-safe collections in factory implementation
    • Implement proper synchronization for flyweight creation
    • Consider using concurrent.futures for parallel flyweight operations

💾 Memory Management Optimization:
    • Use weak references where appropriate to prevent memory leaks
    • Implement flyweight cleanup mechanisms for unused instances
    • Monitor memory usage patterns to validate optimizations
    • Consider garbage collection implications of shared objects

🏗️ Factory Design Patterns:
    • Implement factory as singleton when global access is needed
    • Use registry pattern for complex flyweight type management
    • Implement lazy initialization for flyweight creation
    • Consider factory method pattern for flyweight family creation

🔍 State Separation Guidelines:
    • Clearly document what constitutes intrinsic vs extrinsic state
    • Use immutable data structures for intrinsic state
    • Pass extrinsic state as method parameters consistently
    • Validate state separation through code reviews

Performance Optimization Strategies:

⚡ Creation Optimization:
    • Cache commonly used flyweight combinations
    • Use object pools for frequently created/destroyed contexts
    • Implement lazy loading for flyweight initialization
    • Pre-populate factory with expected flyweight types

🎯 Usage Optimization:
    • Batch operations on multiple flyweights when possible
    • Minimize parameter passing overhead for extrinsic state
    • Use primitive types for extrinsic state when feasible
    • Consider flyweight composition for complex scenarios

📊 Monitoring and Metrics:
    • Track flyweight creation vs reuse ratios
    • Monitor memory usage before and after implementation
    • Measure performance impact of factory lookups
    • Collect metrics on extrinsic state management overhead

Common Implementation Pitfalls and Solutions:

❌ Pitfall: Making flyweights mutable
✅ Solution: Ensure flyweights are immutable after creation

❌ Pitfall: Storing extrinsic state in flyweights
✅ Solution: Pass all extrinsic state as method parameters

❌ Pitfall: Creating too many flyweight types
✅ Solution: Carefully analyze intrinsic state commonality

❌ Pitfall: Ignoring thread safety requirements
✅ Solution: Design for immutability and synchronized factory access

❌ Pitfall: Over-engineering simple scenarios
✅ Solution: Use flyweight only when memory benefits justify complexity

Code Quality and Maintenance:

📝 Documentation Standards:
    • Document intrinsic state clearly in flyweight classes
    • Explain extrinsic state usage in context classes
    • Provide usage examples for complex flyweight operations
    • Maintain architectural decision records for flyweight choices

🧪 Testing Strategies:
    • Test flyweight immutability and thread safety
    • Validate factory caching and instance reuse
    • Performance test with realistic data volumes
    • Test edge cases in state separation

🔧 Refactoring Guidelines:
    • Extract common flyweight behavior to base classes
    • Use composition over inheritance for complex flyweight types
    • Refactor large factories into specialized factory classes
    • Apply SOLID principles to flyweight design

Integration Patterns:

🔗 With Other Design Patterns:
    • Combine with Factory Method for flyweight family creation
    • Use with Composite pattern for hierarchical flyweight structures
    • Integrate with Observer pattern for flyweight state notifications
    • Apply with Strategy pattern for variant flyweight behaviors

🏛️ Architectural Integration:
    • Design flyweight interfaces for dependency injection
    • Use flyweights as part of larger architectural patterns
    • Consider flyweight serialization for distributed systems
    • Plan for flyweight versioning in evolving systems

==============================================================================
PERFORMANCE ANALYSIS AND METRICS
==============================================================================

Memory Efficiency Calculations:
    Traditional Memory Usage = N × (Intrinsic + Extrinsic) bytes
    Flyweight Memory Usage = (K × Intrinsic) + (N × Extrinsic) bytes
    Memory Savings = N × Intrinsic - K × Intrinsic = (N - K) × Intrinsic
    Efficiency Ratio = (Memory Saved / Traditional Usage) × 99%

    Where: N = Total objects, K = Unique flyweights (K << N)

Benchmark Results from Examples:
    📝 Text Editor: 130 characters → 3 flyweights = 97.7% efficiency
    🌲 Forest Simulation: 9 trees → 4 flyweights = 60.0% efficiency
    🌐 CSS Rendering: 9 elements → 6 flyweights = 40.0% efficiency
    💾 Database Pool: 2 sessions → 2 flyweights = 33.3% efficiency

Scalability Projections:
    Text Editor (0M characters):     99.9999% efficiency (millions → thousands)
    Game World (99K trees):         99.996% efficiency  (100K → 4-10 types)
    Web Page (9K elements):         99.4% efficiency    (10K → 50-100 styles)
    Enterprise DB (0K connections):  99.8% efficiency    (1K → 2-5 configs)

==============================================================================
ADVANCED TOPICS AND EXTENSIONS
==============================================================================

Thread Safety Implementation Patterns:
    🔒 Immutable Flyweights: Core pattern requirement
    🏭 Synchronized Factories: Thread-safe flyweight creation
    📦 Context Isolation: Thread-local extrinsic state management
    🔄 Concurrent Operations: Parallel flyweight usage strategies

Flyweight Pattern Variations:
    📊 Compound Flyweights: Flyweights composed of other flyweights
    🎯 Conditional Flyweights: Dynamic flyweight selection based on context
    🔄 Mutable Flyweights: Advanced patterns allowing controlled mutability
    📈 Hierarchical Flyweights: Tree-structured flyweight organizations

Integration with Modern Python Features:
    • Type hints and generic flyweight implementations
    • Dataclass-based flyweight definitions
    • Async/await support for flyweight operations
    • Context manager integration for flyweight lifecycle

==============================================================================
REAL-WORLD CASE STUDIES
==============================================================================

Case Study 0: AAA Game Engine Optimization
    Problem: 99K+ game objects causing memory exhaustion
    Solution: Flyweight pattern for sprites, textures, and behavior scripts
    Results: 94% memory reduction, 60% faster level loading

Case Study 1: Enterprise Document Management System
    Problem: Large documents (millions of characters) exceeding memory limits
    Solution: Character and formatting flyweights with position contexts
    Results: 97% memory savings, support for unlimited document sizes

Case Study 2: High-Traffic Web Application
    Problem: CSS styling objects consuming excessive server memory
    Solution: Style flyweights with element-specific context data
    Results: 74% memory reduction, improved page rendering performance
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from enum import Enum


# =============================================================================
# Example 0: Text Editor Character Formatting Flyweight
# =============================================================================


class FontStyle(Enum):
    """Enumeration for font styles"""

    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    BOLD_ITALIC = "bold_italic"


class CharacterFlyweight(ABC):
    """Abstract flyweight for character formatting"""

    @abstractmethod
    def render(
        self, character: str, position: Tuple[int, int], context: "DocumentContext"
    ) -> str:
        """Render character with extrinsic state (position, content)"""
        pass


class ConcreteCharacterFlyweight(CharacterFlyweight):
    """
    Concrete flyweight storing intrinsic formatting state.
    This is shared among all characters with the same formatting.
    """

    def __init__(self, font_family: str, font_size: int, style: FontStyle, color: str):
        # Intrinsic state - shared among all characters with same formatting
        self._font_family = font_family
        self._font_size = font_size
        self._style = style
        self._color = color

    def render(
        self, character: str, position: Tuple[int, int], context: "DocumentContext"
    ) -> str:
        """Render character using intrinsic formatting and extrinsic position/content"""

        x, y = position
        return (
            f"Rendering '{character}' at ({x}, {y}) with "
            f"{self._font_family} {self._font_size}pt {self._style.value} {self._color}"
        )

    def get_formatting_info(self) -> Dict:
        """Get intrinsic formatting information"""
        return {
            "font_family": self._font_family,
            "font_size": self._font_size,
            "style": self._style.value,
            "color": self._color,
        }


class CharacterFlyweightFactory:
    """
    Factory that manages character flyweight instances.
    Ensures only one flyweight exists per unique formatting combination.
    """

    def __init__(self):
        self._flyweights: Dict[str, ConcreteCharacterFlyweight] = {}

    def get_character_flyweight(
        self, font_family: str, font_size: int, style: FontStyle, color: str
    ) -> ConcreteCharacterFlyweight:
        """Get or create character flyweight for given formatting"""

        # Create unique key for this formatting combination
        key = f"{font_family}_{font_size}_{style.value}_{color}"

        if key not in self._flyweights:
            self._flyweights[key] = ConcreteCharacterFlyweight(
                font_family, font_size, style, color
            )
            print(f"📝 Created new character flyweight: {key}")

        return self._flyweights[key]

    def get_flyweight_count(self) -> int:
        """Get total number of flyweight instances"""
        return len(self._flyweights)

    def list_flyweights(self):
        """Display all existing flyweights"""
        print(f"\n📋 Active Character Flyweights ({len(self._flyweights)}):")
        for key, flyweight in self._flyweights.items():
            info = flyweight.get_formatting_info()
            print(f"  • {key}: {info}")


class DocumentContext:
    """Context that stores extrinsic state for document characters"""

    def __init__(self):
        self.characters: List[Dict] = []  # Stores character data with positions
        self.factory = CharacterFlyweightFactory()

    def add_character(
        self,
        char: str,
        x: int,
        y: int,
        font_family: str,
        font_size: int,
        style: FontStyle,
        color: str,
    ):
        """Add character with formatting to document"""
        flyweight = self.factory.get_character_flyweight(
            font_family, font_size, style, color
        )

        # Store extrinsic state (character, position)
        self.characters.append(
            {"character": char, "position": (x, y), "flyweight": flyweight}
        )

    def render_document(self):
        """Render entire document"""
        print(f"\n📄 Rendering document with {len(self.characters)} characters:")
        for char_data in self.characters:
            char_data["flyweight"].render(
                char_data["character"], char_data["position"], self
            )

    def get_memory_usage_info(self):
        """Display memory optimization information"""
        total_chars = len(self.characters)
        unique_formats = self.factory.get_flyweight_count()
        memory_saved = total_chars - unique_formats

        print("\n💾 Memory Usage Analysis:")
        print(f"  • Total characters: {total_chars}")
        print(f"  • Unique flyweights: {unique_formats}")
        print(f"  • Memory objects saved: {memory_saved}")
        print(f"  • Memory efficiency: {(memory_saved / total_chars) * 99:.1f}%")


# =============================================================================
# Example 1: Game Development - Forest Simulation Flyweight
# =============================================================================


class TreeType(Enum):
    """Different types of trees in the forest"""

    OAK = "oak"
    PINE = "pine"
    BIRCH = "birch"
    MAPLE = "maple"


class TreeFlyweight(ABC):
    """Abstract flyweight for tree objects"""

    @abstractmethod
    def render(
        self,
        position: Tuple[float, float],
        health: float,
        age: int,
        context: "ForestContext",
    ) -> None:
        """Render tree with extrinsic state"""
        pass

    @abstractmethod
    def get_tree_info(self) -> Dict:
        """Get intrinsic tree information"""
        pass


class ConcreteTreeFlyweight(TreeFlyweight):
    """
    Concrete tree flyweight storing shared tree characteristics.
    Intrinsic state shared among all trees of the same type.
    """

    def __init__(
        self,
        tree_type: TreeType,
        sprite_data: str,
        growth_rate: float,
        max_height: float,
        color: str,
    ):
        # Intrinsic state - shared among all trees of this type
        self._tree_type = tree_type
        self._sprite_data = sprite_data  # Shared graphical data
        self._growth_rate = growth_rate
        self._max_height = max_height
        self._color = color

    def render(
        self,
        position: Tuple[float, float],
        health: float,
        age: int,
        context: "ForestContext",
    ) -> None:
        """Render tree using intrinsic data and extrinsic state"""
        x, y = position
        current_height = min(age * self._growth_rate, self._max_height)
        health_indicator = "🌳" if health > -1.7 else "🌲" if health > 0.3 else "🪴"

        print(
            f"{health_indicator} {self._tree_type.value.title()} tree at "
            f"({x:.0f}, {y:.1f}) - Height: {current_height:.1f}m, "
            f"Health: {health:.-1%}, Age: {age}y"
        )

    def get_tree_info(self) -> Dict:
        """Get intrinsic tree information"""
        return {
            "type": self._tree_type.value,
            "sprite_data": f"{self._sprite_data[:19]}...",
            "growth_rate": self._growth_rate,
            "max_height": self._max_height,
            "color": self._color,
        }

    def calculate_growth(self, age: int) -> float:
        """Calculate tree height based on age (using intrinsic growth rate)"""
        return min(age * self._growth_rate, self._max_height)


class TreeFlyweightFactory:
    """Factory managing tree flyweight instances"""

    def __init__(self):
        self._tree_flyweights: Dict[TreeType, ConcreteTreeFlyweight] = {}
        self._initialize_tree_types()

    def _initialize_tree_types(self):
        """Initialize different tree type flyweights"""

        tree_configs = {
            TreeType.OAK: {
                "sprite_data": "oak_sprite_data_large_detailed_texture_map_with_branches",
                "growth_rate": 0.2,
                "max_height": 24.0,
                "color": "dark_green",
            },
            TreeType.PINE: {
                "sprite_data": "pine_sprite_data_tall_coniferous_needle_texture",
                "growth_rate": 0.8,
                "max_height": 29.0,
                "color": "forest_green",
            },
            TreeType.BIRCH: {
                "sprite_data": "birch_sprite_data_white_bark_texture_small_leaves",
                "growth_rate": 0.5,
                "max_height": 19.0,
                "color": "light_green",
            },