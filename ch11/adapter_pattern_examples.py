"""
Adapter Design Pattern - Real-World Examples

The Adapter pattern allows incompatible interfaces to work together.
It acts as a bridge between two incompatible interfaces by wrapping
one interface to make it compatible with another.

Key Characteristics:
    - Allows incompatible interfaces to work together
    - Wraps existing functionality with a new interface
    - Enables legacy code integration without modification
    - Acts as a translator between different APIs

When to Use:
    - Integrating third-party libraries with different interfaces
    - Working with legacy systems
    - Making incompatible APIs work together
    - Converting data formats or protocols
"""

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Dict, List, Any


# =============================================================================
# Example 1: Payment Processing Adapter
# =============================================================================


class PaymentProcessor(ABC):
    """
    Standard payment interface that our application expects.

    This abstract base class defines the uniform interface that all payment
    processors in our application must implement. It ensures consistency
    across different payment providers regardless of their underlying APIs.

    Methods:
        process_payment: Process a payment with standardized parameters and return format.
    """

    @abstractmethod
    def process_payment(self, amount: float, card_info: Dict) -> Dict:
        """
        Process a payment transaction.

        Args:
            amount (float): The payment amount in dollars (e.g., 99.99).
            card_info (Dict): Payment information containing:
                - 'token': Card token for secure processing
                - 'email': Customer email for payment confirmation
                - Other provider-specific fields as needed

        Returns:
            Dict: Standardized payment result containing:
                - 'transaction_id': Unique identifier for the transaction
                - 'status': Payment status ('success' or 'failed')
                - 'amount': Amount actually charged
                - 'provider': Name of the payment provider used

        Raises:
            NotImplementedError: Must be implemented by concrete adapter classes.
        """
        pass


class StripePayment:
    """
    Third-party Stripe payment system with its own interface.

    This class represents the external Stripe API that we want to integrate
    into our application. It has its own method signatures and data formats
    that differ from our standard payment interface.

    Key Differences from our standard:
        - Expects amount in cents instead of dollars
        - Uses card tokens instead of full card info
        - Returns Stripe-specific response format
    """
