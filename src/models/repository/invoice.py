"""Invoice Repository."""

from sqlmodel import Session, select
from src.models.tables import Invoices, Users, Organizations
from uuid import UUID


class InvoiceRepository:
    def __init__(self, session: Session):
        self.session = session

    async def get_all_invoices(self, user_id: UUID):
        organization = self.session.exec(
            select(Organizations).where(Organizations.owner_id == user_id)
        )
        if not organization:
            return []
        statement = (
            select(Invoices)
            .join(Organizations, Invoices.organization_id == Organizations.id)
            .where(Organizations.owner_id == user_id)
        )
        results = await self.session.exec(statement)
        return results.all()

    async def create_invoice(self, invoice_data: dict):
        invoice = Invoices(**invoice_data)
        self.session.add(invoice)
        await self.session.commit()
        await self.session.refresh(invoice)
        return invoice

    async def get_invoice(self, invoice_id: str):
        statement = select(Invoices).where(Invoices.id == invoice_id)
        result = await self.session.exec(statement)
        return result.one_or_none()
