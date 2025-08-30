"""Invoice schema."""

from pydantic import BaseModel, Field


# class InvoiceItemsSchema(BaseModel):


class InvoiceCreateSchema(BaseModel):
    """Invoice schema."""

    id: str = Field(default=None)
    organization_id: str
    customer_id: str
    amount: float
    status: str

    class Config:
        """Pydantic config."""

        orm_mode = True
