from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import date

from project.infrastructure.postgres.models import Movement
from project.schemas.movement import MovementSchema
from project.core.config import settings


class MovementRepository:
    _collection: Type[Movement] = Movement

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_movements(self, session: AsyncSession) -> list[MovementSchema]:
        query = text("SELECT * FROM movements;")
        result = await session.execute(query)
        return [MovementSchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_movement_by_id(self, session: AsyncSession, id_movement: int) -> Optional[MovementSchema]:
        query = text("SELECT * FROM movements WHERE id = :id;")
        result = await session.execute(query, {"id": id_movement})
        row = result.mappings().first()
        return MovementSchema.model_validate(dict(row)) if row else None

    async def insert_movement(self, session: AsyncSession,
                             id: int,
                             product_id: int,
                             quantity: int,
                             from_storage_place_id: int,
                             to_storage_place_id: int,
                             movement_date: date) -> Optional[MovementSchema]:
        query = text("""
            INSERT INTO movements (product_id, quantity, from_storage_place_id, to_storage_place_id, movement_date)
            VALUES (:product_id, :quantity, :from_storage_place_id, :to_storage_place_id, :movement_date)
            RETURNING id, product_id, quantity, from_storage_place_id, to_storage_place_id, movement_date;
        """)
        result = await session.execute(query, {
            "product_id": product_id,
            "quantity": quantity,
            "from_storage_place_id": from_storage_place_id,
            "to_storage_place_id": to_storage_place_id,
            "movement_date": movement_date})
        row = result.mappings().first()
        return MovementSchema.model_validate(dict(row)) if row else None



    async def update_movement_by_id(self, session: AsyncSession,
                             id_movement: int,
                             product_id: int,
                             quantity: int,
                             from_storage_place_id: int,
                             to_storage_place_id: int,
                             movement_date: date) -> Optional[MovementSchema]:
        query = text("""
            UPDATE movements
            SET product_id = :product_id, quantity = :quantity, from_storage_place_id = :from_storage_place_id, to_storage_place_id = :to_storage_place_id, movement_date = :movement_date
            WHERE id = :id
            RETURNING id, product_id, quantity, from_storage_place_id, to_storage_place_id, movement_date;
        """)
        result = await session.execute(query, {
            "id": id_movement,
            "product_id": product_id,
            "quantity": quantity,
            "from_storage_place_id": from_storage_place_id,
            "to_storage_place_id": to_storage_place_id,
            "movement_date": movement_date})
        row = result.mappings().first()
        return MovementSchema.model_validate(dict(row)) if row else None

    async def delete_movement_by_id(self, session: AsyncSession, id_movement: int) -> bool:
        query = text("DELETE FROM movements WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_movement})
        row = result.fetchone()
        return row is not None