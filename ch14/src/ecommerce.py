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
