"""DB tables."""

import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlmodel import (
    Field,
    Relationship,
    Session,
    SQLModel,
    create_engine,
)

from src.settings import settings

from .enums import (
    InvoiceStatus,
    PaymentMethod,
    ReminderStatus,
    ReminderType,
    TransactionStatus,
)

# sqlite database
engine = create_engine(
    settings.DATABASE.database_url,
)


# Base class for common fields
class BaseModel(SQLModel):
    """Base model with common fields."""

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    created_at: datetime = Field(
        default_factory=datetime.now(tz=timezone.utc),
    )
    updated_at: datetime = Field(
        default_factory=datetime.now(tz=timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(tz=timezone.utc)},
    )


class Users(BaseModel, table=True):
    """User Table."""

    __tablename__ = "users"

    phone_number: str = Field(
        unique=True,
        index=True,
        max_length=20,
    )
    name: str = Field(max_length=100)
    email: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=255,
    )
    is_active: bool = Field(default=True)
    last_login: Optional[datetime] = Field(  # noqa: FA100
        default=None,
    )

    # Relationships
    owned_organizations: list["Organizations"] = Relationship(back_populates="owner")
    created_invoices: list["Invoices"] = Relationship(back_populates="creator")
    sent_reminders: list["Reminders"] = Relationship(back_populates="sender")


class Organizations(BaseModel, table=True):
    """User Organizations Table. This is meant to be either store/workspace."""

    __tablename__ = "organizations"

    owner_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)  # noqa: FA100
    business_type: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=100,
    )
    contact_email: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=255,
    )
    contact_phone: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=20,
    )

    # Address fields
    address_line1: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=255,
    )
    address_line2: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=255,
    )
    city: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=100,
    )
    state: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=100,
    )
    postal_code: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=20,
    )
    country: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=100,
    )

    is_active: bool = Field(default=True)

    # Relationships
    owner: Users = Relationship(back_populates="owned_organizations")
    customers: list["Customers"] = Relationship(back_populates="organization")
    services: list["Services"] = Relationship(back_populates="organization")
    invoices: list["Invoices"] = Relationship(back_populates="organization")


# Customers table
class Customers(BaseModel, table=True):
    """Customer table."""

    __tablename__ = "customers"

    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id",
        index=True,
    )
    customer_code: str = Field(
        unique=True,
        index=True,
        max_length=50,
    )
    name: str = Field(max_length=255)
    email: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=255,
    )
    phone: str = Field(
        default=None,
        max_length=20,
    )

    # Address fields
    address_line: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=255,
    )
    city: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=100,
    )
    state: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=100,
    )
    postal_code: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=20,
    )
    country: Optional[str] = Field(  # noqa: FA100
        default=None,
        max_length=100,
    )

    is_active: bool = Field(default=True)

    # Relationships
    organization: Organizations = Relationship(back_populates="customers")
    invoices: list["Invoices"] = Relationship(back_populates="customer")
    transactions: list["Transactions"] = Relationship(back_populates="customer")
    reminders: list["Reminders"] = Relationship(back_populates="customer")


# Services table
class Services(BaseModel, table=True):
    """Organization Services table."""

    __tablename__ = "services"

    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id",
        index=True,
    )
    name: str = Field(max_length=255)
    description: Optional[str] = Field(  # noqa: FA100
        default=None,
    )
    cost: Decimal = Field(
        decimal_places=2,
        max_digits=10,
    )
    currency: str = Field(
        default="USD",
        max_length=3,
    )
    is_active: bool = Field(default=True)

    # Relationships
    organization: Organizations = Relationship(back_populates="services")
    invoice_items: list["InvoiceItems"] = Relationship(back_populates="service")


# Invoices table
class Invoices(BaseModel, table=True):
    """Oraganization Invoice."""

    __tablename__ = "invoices"

    invoice_number: str = Field(
        unique=True,
        index=True,
        max_length=50,
    )
    customer_id: uuid.UUID = Field(
        foreign_key="customers.id",
        index=True,
    )
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id",
        index=True,
    )
    created_by: uuid.UUID = Field(
        foreign_key="users.id",
        index=True,
    )

    subtotal: Decimal = Field(
        decimal_places=2,
        max_digits=12,
    )
    tax_amount: Decimal = Field(
        default=0,
        decimal_places=2,
        max_digits=12,
    )
    total_amount: Decimal = Field(
        decimal_places=2,
        max_digits=12,
        default=Decimal("0.00"),
    )
    currency: str = Field(
        default="TZS",
        max_length=3,
    )

    status: InvoiceStatus = Field(
        default=InvoiceStatus.DRAFT,
    )
    issue_date: date = Field(
        default_factory=date.today,
    )
    due_date: Optional[date] = Field(  # noqa: FA100
        default=None,
    )

    # Relationships
    customer: Customers = Relationship(back_populates="invoices")
    organization: Organizations = Relationship(back_populates="invoices")
    creator: Users = Relationship(back_populates="created_invoices")
    invoice_items: list["InvoiceItems"] = Relationship(back_populates="invoice")
    transactions: list["Transactions"] = Relationship(back_populates="invoice")
    reminders: list["Reminders"] = Relationship(back_populates="invoice")


# Invoice Items table
class InvoiceItems(BaseModel, table=True):
    """ "Invoice item."""

    __tablename__ = "invoice_items"

    invoice_id: uuid.UUID = Field(
        foreign_key="invoices.id",
        index=True,
    )
    service_id: Optional[uuid.UUID] = Field(  # noqa: FA100
        foreign_key="services.id",
        default=None,
    )
    description: str = Field(
        max_length=500,
    )
    quantity: Decimal = Field(
        decimal_places=2,
        max_digits=10,
    )
    unit_price: Decimal = Field(
        decimal_places=2,
        max_digits=10,
    )
    total_amount: Decimal = Field(
        decimal_places=2,
        max_digits=12,
    )

    # Relationships
    invoice: Invoices = Relationship(back_populates="invoice_items")
    service: Optional[Services] = Relationship(back_populates="invoice_items")


# Transactions table
class Transactions(BaseModel, table=True):
    """Transactions."""

    __tablename__ = "transactions"

    transaction_number: str = Field(
        unique=True,
        index=True,
        max_length=50,
    )
    invoice_id: uuid.UUID = Field(
        foreign_key="invoices.id",
        index=True,
    )
    customer_id: uuid.UUID = Field(
        foreign_key="customers.id",
        index=True,
    )

    amount: Decimal = Field(
        decimal_places=2,
        max_digits=12,
    )
    currency: str = Field(
        default="USD",
        max_length=3,
    )
    payment_method: PaymentMethod = Field(
        default=PaymentMethod.CASH,
    )
    status: TransactionStatus = Field(
        default=TransactionStatus.PENDING,
    )
    reference_number: Optional[str] = Field(
        default=None,
        max_length=100,
    )
    notes: Optional[str] = Field(  # noqa: FA100
        default=None,
    )
    transaction_date: datetime = Field(
        default_factory=datetime.now(tz=timezone.utc),
    )

    # Relationships
    invoice: Invoices = Relationship(back_populates="transactions")
    customer: Customers = Relationship(back_populates="transactions")


# Reminders table
class Reminders(BaseModel, table=True):
    """Customer Reminder."""

    __tablename__ = "reminders"

    invoice_id: uuid.UUID = Field(foreign_key="invoices.id", index=True)
    customer_id: uuid.UUID = Field(foreign_key="customers.id", index=True)
    sent_by: uuid.UUID = Field(foreign_key="users.id", index=True)

    type: ReminderType = Field(default=ReminderType.SMS)
    status: ReminderStatus = Field(default=ReminderStatus.PENDING)
    message: str = Field(max_length=1000)
    sent_at: Optional[datetime] = Field(default=None)
    scheduled_for: Optional[datetime] = Field(default=None)

    # Relationships
    invoice: Invoices = Relationship(back_populates="reminders")
    customer: Customers = Relationship(back_populates="reminders")
    sender: Users = Relationship(back_populates="sent_reminders")


# OTP Verification table (for phone verification)
class OTPVerifications(BaseModel, table=True):
    __tablename__ = "otp_verifications"

    phone: str = Field(max_length=20, index=True)
    otp_code: str = Field(max_length=6)
    is_verified: bool = Field(default=False)
    expires_at: datetime
    attempts: int = Field(default=0)

    class Config:
        # Auto-delete expired OTPs
        table_args = {"sqlite_autoincrement": True}


SQLModel.metadata.create_all(engine)


#  session dependencies
def get_session() -> Session:
    """Get database session."""
    with Session(engine) as session:
        yield session
