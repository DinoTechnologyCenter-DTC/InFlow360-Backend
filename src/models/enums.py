"""Supported Enums."""

from enum import Enum


# Enums for status fields
class InvoiceStatus(str, Enum):
    """Invoice status."""

    DRAFT = "DRAFT"
    SENT = "SENT"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"


class TransactionStatus(str, Enum):
    """Transaction Status Enum."""

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class PaymentMethod(str, Enum):
    """Payment Method Enum."""

    CASH = "CASH"
    CARD = "CARD"
    BANK_TRANSFER = "BANK_TRANSFER"
    MOBILE_MONEY = "MOBILE_MONEY"


class UserRole(str, Enum):
    """User Role Enum."""

    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    STAFF = "STAFF"


class ReminderType(str, Enum):
    """Reminder Type Enum."""

    SMS = "SMS"
    EMAIL = "EMAIL"
    CALL = "CALL"


class ReminderStatus(str, Enum):
    """Reminder Status Enum."""

    PENDING = "PENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"


__all__ = [
    "InvoiceStatus",
    "PaymentMethod",
    "ReminderStatus",
    "ReminderType",
    "TransactionStatus",
]
