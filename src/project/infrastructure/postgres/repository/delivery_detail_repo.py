from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import date

from project.infrastructure.postgres.models import DeliveryDetail
from project.schemas.delivery_detail import DeliveryDetailSchema
from project.core.config import settings


class DeliveryDetailRepository:
    _collection: Type[DeliveryDetail] = DeliveryDetail

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_delivery_details(self, session: AsyncSession) -> list[DeliveryDetailSchema]:
        query = text("SELECT * FROM delivery_details;")
        result = await session.execute(query)
        return [DeliveryDetailSchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_delivery_detail_by_id(self, session: AsyncSession, id_delivery_detail: int) -> Optional[DeliveryDetailSchema]:
        query = text("SELECT * FROM delivery_details WHERE id = :id;")
        result = await session.execute(query, {"id": id_delivery_detail})
        row = result.mappings().first()
        return DeliveryDetailSchema.model_validate(dict(row)) if row else None

    async def insert_delivery_detail(self, session: AsyncSession,
                             id: int,
                             delivery_id: int,
                             product_id: int,
                             quantity: int,
                             price: float) -> Optional[DeliveryDetailSchema]:
        query = text("""
            INSERT INTO delivery_details (delivery_id, product_id, quantity, price)
            VALUES (:delivery_id, :product_id, :quantity, :price)
            RETURNING id, delivery_id, product_id, quantity, price;
        """)
        result = await session.execute(query, {
            "delivery_id": delivery_id,
            "product_id": product_id,
            "quantity": quantity,
            "price": price})
        row = result.mappings().first()
        return DeliveryDetailSchema.model_validate(dict(row)) if row else None



    async def update_delivery_detail_by_id(self, session: AsyncSession,
                             id_delivery_detail: int,
                             delivery_id: int,
                             product_id: int,
                             quantity: int,
                             price: float) -> Optional[DeliveryDetailSchema]:
        query = text("""
            UPDATE delivery_details
            SET delivery_id = :delivery_id, product_id = :product_id, quantity = :quantity, price = :price
            WHERE id = :id
            RETURNING id, delivery_id, product_id, quantity, price;
        """)
        result = await session.execute(query, {
            "id": id_delivery_detail,
            "delivery_id": delivery_id,
            "product_id": product_id,
            "quantity": quantity,
            "price": price})
        row = result.mappings().first()
        return DeliveryDetailSchema.model_validate(dict(row)) if row else None

    async def delete_delivery_detail_by_id(self, session: AsyncSession, id_delivery_detail: int) -> bool:
        query = text("DELETE FROM delivery_details WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_delivery_detail})
        row = result.fetchone()
        return row is not None