from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import date

from project.infrastructure.postgres.models import Shipment
from project.schemas.shipment import ShipmentSchema
from project.core.config import settings


class ShipmentRepository:
    _collection: Type[Shipment] = Shipment

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_shipments(self, session: AsyncSession) -> list[ShipmentSchema]:
        query = text("SELECT * FROM shipments;")
        result = await session.execute(query)
        return [ShipmentSchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_shipment_by_id(self, session: AsyncSession, id_shipment: int) -> Optional[ShipmentSchema]:
        query = text("SELECT * FROM shipments WHERE id = :id;")
        result = await session.execute(query, {"id": id_shipment})
        row = result.mappings().first()
        return ShipmentSchema.model_validate(dict(row)) if row else None

    async def insert_shipment(self, session: AsyncSession,
                             id: int,
                             address: str,
                             total_sum: float,
                             warehouse_id: int,
                             client_id: int,
                             shipment_date: date) -> Optional[ShipmentSchema]:
        query = text("""
            INSERT INTO shipments (address, total_sum, warehouse_id, client_id, shipment_date)
            VALUES (:address, :total_sum, :warehouse_id, :client_id, :shipment_date)
            RETURNING id, address, total_sum, warehouse_id, client_id, shipment_date;
        """)
        result = await session.execute(query, {
            "address": address,
            "total_sum": total_sum,
            "warehouse_id": warehouse_id,
            "client_id": client_id,
            "shipment_date": shipment_date})
        row = result.mappings().first()
        return ShipmentSchema.model_validate(dict(row)) if row else None



    async def update_shipment_by_id(self, session: AsyncSession,
                             id_shipment: int,
                             address: str,
                             total_sum: float,
                             warehouse_id: int,
                             client_id: int,
                             shipment_date: date) -> Optional[ShipmentSchema]:
        query = text("""
            UPDATE shipments
            SET address = :address, total_sum = :total_sum, warehouse_id = :warehouse_id, client_id = :client_id, shipment_date = :shipment_date
            WHERE id = :id
            RETURNING id, address, total_sum, warehouse_id, client_id, shipment_date;
        """)
        result = await session.execute(query, {
            "id": id_shipment,
            "address": address,
            "total_sum": total_sum,
            "warehouse_id": warehouse_id,
            "client_id": client_id,
            "shipment_date": shipment_date})
        row = result.mappings().first()
        return ShipmentSchema.model_validate(dict(row)) if row else None

    async def delete_shipment_by_id(self, session: AsyncSession, id_shipment: int) -> bool:
        query = text("DELETE FROM shipments WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_shipment})
        row = result.fetchone()
        return row is not None