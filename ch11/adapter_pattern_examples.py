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

    def __init__(self, stripe_payment: StripePayment):
        """
        Initialize the Stripe adapter.

        Args:
            stripe_payment (StripePayment): The Stripe payment instance to wrap.
        """

        self.stripe_payment = stripe_payment

    def process_payment(self, amount: float, card_info: Dict) -> Dict:
        """
        Convert our standard interface to Stripe's interface.

        This method performs the core adapter functionality:
        1. Converts input parameters from our format to Stripe's format
        2. Calls the wrapped Stripe payment method
        3. Converts the response from Stripe's format to our format

        Args:
            amount (float): Payment amount in dollars.
            card_info (Dict): Our standard card info format.

        Returns:
            Dict: Our standardized response format.

        Example:
            >>> adapter.process_payment(99.99, {'token': 'card_123'})
            {'transaction_id': 'stripe_txn_9999', 'status': 'success',
             'amount': 99.99, 'provider': 'Stripe'}
        """

        # Convert dollars to cents
        amount_cents = int(amount * 100)

        # Extract card token from our format
        card_token = card_info.get("token", "default_token")

        # Call Stripe's method with converted parameters
        stripe_result = self.stripe_payment.charge_card(amount_cents, card_token)

        # Convert Stripe's response to our standard format
        return {
            "transaction_id": stripe_result["stripe_transaction_id"],
            "status": "success" if stripe_result["status"] == "completed" else "failed",
            "amount": stripe_result["amount_charged"],
            "provider": "Stripe",
        }


class PayPalAdapter(PaymentProcessor):
    """Adapter to make PayPal compatible with our standard interface"""

    def __init__(self, paypal_payment: PayPalPayment):
        self.paypal_payment = paypal_payment

    def process_payment(self, amount: float, card_info: Dict) -> Dict:
        """Convert our standard interface to PayPal's interface"""

        # Extract email from our card info
        account_email = card_info.get("email", "user@example.com")

        # Call PayPal's method
        paypal_result = self.paypal_payment.make_payment(amount, account_email)

        # Convert PayPal's response to our standard format
        return {
            "transaction_id": paypal_result["paypal_reference"],
            "status": "success"
            if paypal_result["payment_status"] == "success"
            else "failed",
            "amount": paypal_result["charged_amount"],
            "provider": "PayPal",
        }


# =============================================================================
# Example 2: Data Format Adapter (XML to JSON)
# =============================================================================


class DataProcessor:
    """
    Our application expects to work with JSON data.

    This class represents our application's data processing component
    that is designed to work with JSON format data. It demonstrates
    the "target" interface that we want to maintain consistent.
    """

    def process_json_data(self, json_data: str) -> Dict:
        """
        Standard method that expects JSON format.

        Args:
            json_data (str): JSON formatted string containing data to process.

        Returns:
            Dict: Processing result containing:
                - 'processed': Boolean indicating successful processing
                - 'record_count': Number of records processed
                - 'data': The actual processed data

        Example:
            >>> processor = DataProcessor()
            >>> result = processor.process_json_data('[{"name": "Alice"}]')
            >>> print(result['record_count'])  # 1
        """

        data = json.loads(json_data)
        return {
            "processed": True,
            "record_count": len(data) if isinstance(data, list) else 1,
            "data": data,
        }


class LegacyXMLSystem:
    """
    Legacy system that only provides XML data.

    This class represents an older system that we cannot modify but need
    to integrate with. It only knows how to work with XML format, which
    is incompatible with our modern JSON-based application.

    Real-world examples:
        - Old enterprise systems
        - Legacy databases with XML export
        - Third-party services with only XML APIs
        - Government or institutional data sources
    """

    def get_xml_data(self) -> str:
        """
        Returns data in XML format.

        Returns:
            str: XML formatted string containing user data.

        Note:
            This simulates a legacy system that can only provide XML.
            In real scenarios, this might be reading from old databases,
            calling legacy SOAP services, or parsing XML files.
        """
        return """<?xml version="1.0"?>
        <users>
            <user>
                <id>1</id>
                <name>Alice</name>
                <email>alice@example.com</email>
            </user>
            <user>
                <id>2</id>
                <name>Bob</name>
                <email>bob@example.com</email>
            </user>
        </users>"""
