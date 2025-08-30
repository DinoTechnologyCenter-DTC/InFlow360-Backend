"""Invoice API Router."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.models.tables import Session, get_session
from src.services.auth import get_current_user

router = APIRouter()


@router.get("/")
async def get_invoices(
    session: Annotated[Session, Depends(get_session)],
    user: Annotated[bool, Depends(get_current_user)],
):
    """Get all invoices."""
    # Logic to retrieve all invoices
    return {"status": "success", "data": []}


@router.post("/")
async def create_invoice(
    invoice_data: dict,
    session: Annotated[Session, Depends(get_session)],
    user: Annotated[bool, Depends(get_current_user)],
):
    """Create a new invoice."""
    # Logic to create an invoice
    return {"status": "success", "data": invoice_data}


@router.get("/{invoice_id}")
async def get_invoice(
    invoice_id: str,
    session: Annotated[Session, Depends(get_session)],
    user: Annotated[bool, Depends(get_current_user)],
):
    """Get an invoice by ID."""
    # Logic to retrieve an invoice
    return {"status": "success", "data": {"invoice_id": invoice_id}}
