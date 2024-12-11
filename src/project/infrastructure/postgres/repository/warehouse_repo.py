from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.infrastructure.postgres.models import Warehouse
from project.schemas.warehouse import WarehouseSchema
from project.core.config import settings


class WarehouseRepository:
    _collection: Type[Warehouse] = Warehouse

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_warehouses(self, session: AsyncSession) -> list[WarehouseSchema]:
        query = text("SELECT * FROM warehouses;")
        result = await session.execute(query)
        return [WarehouseSchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_warehouse_by_id(self, session: AsyncSession, id_warehouse: int) -> Optional[WarehouseSchema]:
        query = text("SELECT * FROM warehouses WHERE id = :id;")
        result = await session.execute(query, {"id": id_warehouse})
        row = result.mappings().first()
        return WarehouseSchema.model_validate(dict(row)) if row else None

    async def insert_warehouse(self, session: AsyncSession,
                             id: int,
                             available_types: str,
                             address: str,
                             name: str,
                             available_places: int) -> Optional[WarehouseSchema]:
        query = text("""
            INSERT INTO warehouses (available_types, address, name, available_places)
            VALUES (:available_types, :address, :name, :available_places)
            RETURNING id, available_types, address, name, available_places;
        """)
        result = await session.execute(query, {
            "available_types": available_types,
            "address": address,
            "name": name,
            "available_places": available_places})
        row = result.mappings().first()
        return WarehouseSchema.model_validate(dict(row)) if row else None



    async def update_warehouse_by_id(self, session: AsyncSession,
                             id_warehouse: int,
                             available_types: str,
                             address: str,
                             name: str,
                             available_places: int) -> Optional[WarehouseSchema]:
        query = text("""
            UPDATE warehouses
            SET available_types = :available_types, address = :address, name = :name, available_places = :available_places
            WHERE id = :id
            RETURNING id, available_types, address, name, available_places;
        """)
        result = await session.execute(query, {
            "id": id_warehouse,
            "available_types": available_types,
            "address": address,
            "name": name,
            "available_places": available_places})
        row = result.mappings().first()
        return WarehouseSchema.model_validate(dict(row)) if row else None

    async def delete_warehouse_by_id(self, session: AsyncSession, id_warehouse: int) -> bool:
        query = text("DELETE FROM warehouses WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_warehouse})
        row = result.fetchone()
        return row is not None