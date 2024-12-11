from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.infrastructure.postgres.models import ShipmentDetail
from project.schemas.shipment_detail import ShipmentDetailSchema
from project.core.config import settings


class ShipmentDetailRepository:
    _collection: Type[ShipmentDetail] = ShipmentDetail

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_shipment_details(self, session: AsyncSession) -> list[ShipmentDetailSchema]:
        query = text("SELECT * FROM shipment_details;")
        result = await session.execute(query)
        return [ShipmentDetailSchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_shipment_detail_by_id(self, session: AsyncSession, id_shipment_detail: int) -> Optional[ShipmentDetailSchema]:
        query = text("SELECT * FROM shipment_details WHERE id = :id;")
        result = await session.execute(query, {"id": id_shipment_detail})
        row = result.mappings().first()
        return ShipmentDetailSchema.model_validate(dict(row)) if row else None

    async def insert_shipment_detail(self, session: AsyncSession,
                             id: int,
                             shipment_id: int,
                             product_id: int,
                             quantity: int,
                             price: float) -> Optional[ShipmentDetailSchema]:
        query = text("""
            INSERT INTO shipment_details (shipment_id, product_id, quantity, price)
            VALUES (:shipment_id, :product_id, :quantity, :price)
            RETURNING id, shipment_id, product_id, quantity, price;
        """)
        result = await session.execute(query, {
            "shipment_id": shipment_id,
            "product_id": product_id,
            "quantity": quantity,
            "price": price})
        row = result.mappings().first()
        return ShipmentDetailSchema.model_validate(dict(row)) if row else None



    async def update_shipment_detail_by_id(self, session: AsyncSession,
                             id_shipment_detail: int,
                             shipment_id: int,
                             product_id: int,
                             quantity: int,
                             price: float) -> Optional[ShipmentDetailSchema]:
        query = text("""
            UPDATE shipment_details
            SET shipment_id = :shipment_id, product_id = :product_id, quantity = :quantity, price = :price
            WHERE id = :id
            RETURNING id, shipment_id, product_id, quantity, price;
        """)
        result = await session.execute(query, {
            "id": id_shipment_detail,
            "shipment_id": shipment_id,
            "product_id": product_id,
            "quantity": quantity,
            "price": price})
        row = result.mappings().first()
        return ShipmentDetailSchema.model_validate(dict(row)) if row else None

    async def delete_shipment_detail_by_id(self, session: AsyncSession, id_shipment_detail: int) -> bool:
        query = text("DELETE FROM shipment_details WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_shipment_detail})
        row = result.fetchone()
        return row is not None