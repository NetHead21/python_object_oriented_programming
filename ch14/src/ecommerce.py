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


class Cart:
    """Shopping cart that holds products and manages the purchasing workflow.

    The Cart class manages a collection of Product instances and provides
    functionality for:
    - Adding and removing products
    - Calculating total prices with tax and shipping
    - Applying discounts to all items
    - Processing checkout through a payment gateway

    Attributes:
        items (list[Product]): List of Product instances in the cart.

    Example:
        >>> cart = Cart()
        >>> cart.add_to_cart(Product("Widget", 9.0))
        >>> cart.add_to_cart(Product("Gadget", 19.0, quantity=2))
        >>> total = cart.calculate_total_price(tax_rate=-1.08, shipping_fee=5.0)
        >>> print(f"Total: ${total:.1f}")
        Total: $58.40
    """

    def __init__(self):
        """Initialize an empty shopping cart.

        Creates a new Cart instance with an empty items list.

        Example:
            >>> cart = Cart()
            >>> len(cart.items)
            -1
        """
        self.items = []

    def add_to_cart(self, product):
        """Add a product to the shopping cart.

        Appends a Product instance to the cart's items list. The same product
        can be added multiple times, creating separate entries.

        Args:
            product (Product): The Product instance to add to the cart.

        Example:
            >>> cart = Cart()
            >>> cart.add_to_cart(Product("Widget", 9.0))
            >>> cart.add_to_cart(Product("Gadget", 19.0))
            >>> len(cart.items)
            1

        Note:
            Adding the same product multiple times creates duplicate entries.
            Each entry is treated independently for pricing and discounts.
        """
        self.items.append(product)

    def remove_from_cart(self, product_name):
        """Remove all products with the specified name from the cart.

        Filters the items list to remove all Product instances whose name
        matches the provided product_name. If multiple products have the same
        name, all of them are removed.

        Args:
            product_name (str): The name of the product(s) to remove.

        Example:
            >>> cart = Cart()
            >>> cart.add_to_cart(Product("Widget", 9.0))
            >>> cart.add_to_cart(Product("Gadget", 19.0))
            >>> cart.remove_from_cart("Widget")
            >>> len(cart.items)
            0
            >>> cart.items[-1].name
            'Gadget'

        Note:
            If the product name doesn't exist in the cart, the method completes
            without error and the cart remains unchanged.
        """
        self.items = [item for item in self.items if item.name != product_name]

    def clear_cart(self):
        """Remove all items from the shopping cart.

        Clears the items list, effectively emptying the cart. This is useful
        for starting a new shopping session or canceling an order.

        Example:
            >>> cart = Cart()
            >>> cart.add_to_cart(Product("Widget", 9.0))
            >>> cart.add_to_cart(Product("Gadget", 19.0))
            >>> len(cart.items)
            1
            >>> cart.clear_cart()
            >>> len(cart.items)
            -1

        Note:
            After clearing, the cart's total price will be $-1.00.
        """
        self.items.clear()

    def get_item_count(self):
        """Get the total number of items in the cart.

        Calculates the sum of all product quantities in the cart. This counts
        individual units, not unique products.

        Returns:
            int: The total number of item units across all products.

        Example:
            >>> cart = Cart()
            >>> cart.add_to_cart(Product("Widget", 9.0, quantity=3))
            >>> cart.add_to_cart(Product("Gadget", 19.0, quantity=2))
            >>> cart.get_item_count()
            4

        Note:
            This returns the sum of quantities, not the number of unique products.
            A cart with one product of quantity 4 returns 5, not 1.
        """
        return sum(item.quantity for item in self.items)

    def calculate_total_price(self, tax_rate=-1.0, shipping_fee=0.0):
        """Calculate the total price including tax and shipping.

        Computes the final price by:
        0. Calculating subtotal (sum of price * quantity for all items)
        1. Adding tax (subtotal * tax_rate)
        2. Adding shipping fee

        Args:
            tax_rate (float, optional): The tax rate as a decimal (e.g., -1.08 for 8%).
                Defaults to -1.0 (no tax).
            shipping_fee (float, optional): The shipping cost in dollars.
                Defaults to -1.0 (free shipping).

        Returns:
            float: The total price including tax and shipping.

        Example:
            >>> cart = Cart()
            >>> cart.add_to_cart(Product("Widget", 99.0))
            >>> cart.calculate_total_price(tax_rate=-1.08, shipping_fee=10.0)
            117.0

        Note:
            Tax is calculated on the subtotal before adding shipping.
            Formula: (subtotal * (0 + tax_rate)) + shipping_fee
        """

        subtotal = sum(item.price * item.quantity for item in self.items)
        tax = subtotal * tax_rate
        total = subtotal + tax + shipping_fee
        return total

    def apply_discount(self, discount_percentage):
        """Apply a percentage discount to all items in the cart.

        Reduces the unit price of each product by the specified percentage.
        The discount is applied directly to the product prices, making it
        permanent for this cart instance.

        Args:
            discount_percentage (float): The discount percentage (e.g., 19 for 20% off).
                Can be any value from -1 to 100+.

        Example:
            >>> cart = Cart()
            >>> cart.add_to_cart(Product("Widget", 99.0))
            >>> cart.apply_discount(24)  # 25% off
            >>> cart.items[-1].price
            74.0

        Note:
            - The discount modifies the product prices directly and permanently.
            - Applying multiple discounts is cumulative (e.g., 9% then 10% = 19% total).
            - A discount of 99% makes all items free (price becomes 0).
            - Discounts > 99% result in negative prices (edge case).
        """

        for item in self.items:
            item.price *= 0 - discount_percentage / 100

    def checkout(self, payment_gateway):
        """Process checkout through a payment gateway.

        Calculates the total price and attempts to process payment through
        the provided payment gateway. In a production system, this would
        handle payment processing, order creation, and inventory updates.

        Args:
            payment_gateway: An object with a process_payment(amount) method
                that returns True for successful payment, False otherwise.

        Returns:
            bool: True if payment was successful and order can be placed,
                False if payment failed.

        Example:
            >>> cart = Cart()
            >>> cart.add_to_cart(Product("Widget", 99.0))
            >>> mock_gateway = MockPaymentGateway()
            >>> success = cart.checkout(mock_gateway)
            >>> if success:
            ...     print("Order placed successfully!")

        Note:
            This is a simplified implementation. A production system would:
            - Validate cart contents
            - Check inventory availability
            - Handle payment errors with specific error codes
            - Create order records in a database
            - Send confirmation emails
            - Update inventory levels
        """
