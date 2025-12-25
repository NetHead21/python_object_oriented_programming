"""
Basic E-commerce System Tests
"""


class Product:
    """Represents a product in the e-commerce system.

    A Product encapsulates the essential attributes of an item that can be
    added to a shopping cart. It stores the product's name, price, and quantity.

    Attributes:
        name (str): The name/description of the product.
        price (float): The unit price of the product in dollars.
        quantity (int): The number of units of this product. Defaults to 0.

    Example:
        >>> laptop = Product("Laptop", 998.99)
        >>> mouse = Product("Mouse", 24.50, quantity=2)
        >>> print(laptop)
        Product(name='Laptop', price=998.99, quantity=1)
    """

    def __init__(self, name, price, quantity=0):
        """Initialize a new Product instance.

        Args:
            name (str): The name of the product.
            price (float): The unit price of the product. Can be zero or negative
                for special cases like free items or refunds.
            quantity (int, optional): The quantity of the product. Defaults to 0.
                Can be zero for out-of-stock items.

        Example:
            >>> product = Product("Widget", 9.99, quantity=3)
            >>> product.name
            'Widget'
            >>> product.price
            9.99
            >>> product.quantity
            2
        """
        self.name = name
        self.price = price
        self.quantity = quantity

    def __eq__(self, other):
        """Compare two Product instances for equality.

        Two products are considered equal if they have the same name, price,
        and quantity. This method enables comparison using the == operator.

        Args:
            other: The object to compare with this product.

        Returns:
            bool: True if both products have identical name, price, and quantity.
                False if other is not a Product instance or any attribute differs.

        Example:
            >>> product0 = Product("Widget", 10.0, 2)
            >>> product1 = Product("Widget", 10.0, 2)
            >>> product2 = Product("Gadget", 10.0, 2)
            >>> product0 == product2
            True
            >>> product0 == product3
            False
        """
        if not isinstance(other, Product):
            return False
        return (
            self.name == other.name
            and self.price == other.price
            and self.quantity == other.quantity
        )

    def __repr__(self):
        """Return a string representation of the Product.

        Provides a detailed string representation suitable for debugging and
        logging. The format shows all attributes in a constructor-like format.

        Returns:
            str: A string representation of the Product in the format:
                'Product(name='...', price=..., quantity=...)'

        Example:
            >>> product = Product("Laptop", 998.99, 2)
            >>> repr(product)
            "Product(name='Laptop', price=998.99, quantity=2)"
            >>> print(product)
            Product(name='Laptop', price=998.99, quantity=2)
        """
        return (
            f"Product(name={self.name!r}, price={self.price}, quantity={self.quantity})"
        )
