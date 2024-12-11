from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import date

from project.infrastructure.postgres.models import Delivery
from project.schemas.delivery import DeliverySchema
from project.core.config import settings


class DeliveryRepository:
    _collection: Type[Delivery] = Delivery

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_deliveries(self, session: AsyncSession) -> list[DeliverySchema]:
        query = text("SELECT * FROM deliveries;")
        result = await session.execute(query)
        return [DeliverySchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_delivery_by_id(self, session: AsyncSession, id_delivery: int) -> Optional[DeliverySchema]:
        query = text("SELECT * FROM deliveries WHERE id = :id;")
        result = await session.execute(query, {"id": id_delivery})
        row = result.mappings().first()
        return DeliverySchema.model_validate(dict(row)) if row else None

    async def insert_delivery(self, session: AsyncSession,
                              id: int,
                              total_sum: float,
                              supplier_id: int,
                              delivery_date: date) -> Optional[DeliverySchema]:
        query = text("""
            INSERT INTO deliveries (total_sum, supplier_id, delivery_date)
            VALUES (:total_sum, :supplier_id, :delivery_date)
            RETURNING id, total_sum, supplier_id, delivery_date;
        """)
        result = await session.execute(query, {
            "total_sum": total_sum,
            "supplier_id": supplier_id,
            "delivery_date": delivery_date})
        row = result.mappings().first()
        return DeliverySchema.model_validate(dict(row)) if row else None

    async def update_delivery_by_id(self, session: AsyncSession,
                                    id_delivery: int,
                                    total_sum: float,
                                    supplier_id: int,
                                    delivery_date: date) -> Optional[DeliverySchema]:
        query = text("""
            UPDATE deliveries
            SET total_sum = :total_sum, supplier_id = :supplier_id, delivery_date = :delivery_date
            WHERE id = :id
            RETURNING id, total_sum, supplier_id, delivery_date;
        """)
        result = await session.execute(query, {
            "id": id_delivery,
            "total_sum": total_sum,
            "supplier_id": supplier_id,
            "delivery_date": delivery_date})
        row = result.mappings().first()
        return DeliverySchema.model_validate(dict(row)) if row else None

    async def delete_delivery_by_id(self, session: AsyncSession, id_delivery: int) -> bool:
        query = text("DELETE FROM deliveries WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_delivery})
        row = result.fetchone()
        return row is not None