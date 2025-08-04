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

    def charge_card(self, amount_cents: int, card_token: str) -> Dict:
        """
        Process a payment using Stripe's API format.

        Args:
            amount_cents (int): Payment amount in cents (e.g., 9999 for $99.99).
            card_token (str): Stripe card token for secure processing.

        Returns:
            Dict: Stripe-specific response format:
                - 'stripe_transaction_id': Stripe's transaction identifier
                - 'status': Stripe status ('completed', 'failed', etc.)
                - 'amount_charged': Amount charged in dollars

        Note:
            This simulates the actual Stripe API. In real implementation,
            this would make HTTP requests to Stripe's servers.
        """
        return {
            "stripe_transaction_id": f"stripe_txn_{amount_cents}",
            "status": "completed",
            "amount_charged": amount_cents / 100,
        }


class PayPalPayment:
    """
    Third-party PayPal payment system with different interface.

    This class represents the external PayPal API that has completely
    different method signatures and data formats compared to both
    our standard interface and Stripe's interface.

    Key Differences:
        - Expects amount in dollars (not cents like Stripe)
        - Uses account email instead of card tokens
        - Returns PayPal-specific response format
    """

    def make_payment(self, amount_dollars: float, account_email: str) -> Dict:
        """
        Process a payment using PayPal's API format.

        Args:
            amount_dollars (float): Payment amount in dollars (e.g., 99.99).
            account_email (str): Customer's PayPal account email.

        Returns:
            Dict: PayPal-specific response format:
                - 'paypal_reference': PayPal's transaction reference
                - 'payment_status': PayPal status ('success', 'failed', etc.)
                - 'charged_amount': Amount charged in dollars

        Note:
            This simulates the actual PayPal API. In real implementation,
            this would integrate with PayPal's SDK or REST API.
        """
        return {
            "paypal_reference": f"pp_ref_{int(amount_dollars * 100)}",
            "payment_status": "success",
            "charged_amount": amount_dollars,
        }


class StripeAdapter(PaymentProcessor):
    """
    Adapter to make Stripe compatible with our standard payment interface.

    This adapter implements the Adapter pattern by:
    1. Implementing our standard PaymentProcessor interface
    2. Wrapping a StripePayment instance
    3. Translating between our interface and Stripe's interface
    4. Converting data formats (dollars ↔ cents, response formats)

    Benefits:
        - Allows using Stripe without changing our application code
        - Provides consistent interface alongside other payment providers
        - Handles all format conversions transparently

    Example:
        >>> stripe = StripePayment()
        >>> adapter = StripeAdapter(stripe)
        >>> result = adapter.process_payment(99.99, {'token': 'card_123'})
        >>> print(result['provider'])  # 'Stripe'
    """
