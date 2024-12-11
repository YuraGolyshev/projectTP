from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.infrastructure.postgres.models import Supplier
from project.schemas.supplier import SupplierSchema
from project.core.config import settings


class SupplierRepository:
    _collection: Type[Supplier] = Supplier

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_suppliers(self, session: AsyncSession) -> list[SupplierSchema]:
        query = text("SELECT * FROM suppliers;")
        result = await session.execute(query)
        return [SupplierSchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_supplier_by_id(self, session: AsyncSession, id_supplier: int) -> Optional[SupplierSchema]:
        query = text("SELECT * FROM suppliers WHERE id = :id;")
        result = await session.execute(query, {"id": id_supplier})
        row = result.mappings().first()
        return SupplierSchema.model_validate(dict(row)) if row else None

    async def insert_supplier(self, session: AsyncSession,
                             id: int,
                             name: str) -> Optional[SupplierSchema]:
        query = text("""
            INSERT INTO suppliers (name)
            VALUES (:name)
            RETURNING id, name;
        """)
        result = await session.execute(query, {
            "name": name})
        row = result.mappings().first()
        return SupplierSchema.model_validate(dict(row)) if row else None



    async def update_supplier_by_id(self, session: AsyncSession,
                             id_supplier: int,
                             name: str) -> Optional[SupplierSchema]:
        query = text("""
            UPDATE suppliers
            SET name = :name
            WHERE id = :id
            RETURNING id, name;
        """)
        result = await session.execute(query, {
            "id": id_supplier,
            "name": name})
        row = result.mappings().first()
        return SupplierSchema.model_validate(dict(row)) if row else None

    async def delete_supplier_by_id(self, session: AsyncSession, id_supplier: int) -> bool:
        query = text("DELETE FROM suppliers WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_supplier})
        row = result.fetchone()