from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.infrastructure.postgres.models import StoragePlace
from project.schemas.storage_place import StoragePlaceSchema
from project.core.config import settings


class StoragePlaceRepository:
    _collection: Type[StoragePlace] = StoragePlace

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_storage_places(self, session: AsyncSession) -> list[StoragePlaceSchema]:
        query = text("SELECT * FROM storage_places;")
        result = await session.execute(query)
        return [StoragePlaceSchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_storage_place_by_id(self, session: AsyncSession, id_storage_place: int) -> Optional[StoragePlaceSchema]:
        query = text("SELECT * FROM storage_places WHERE id = :id;")
        result = await session.execute(query, {"id": id_storage_place})
        row = result.mappings().first()
        return StoragePlaceSchema.model_validate(dict(row)) if row else None

    async def insert_storage_place(self, session: AsyncSession,
                             id: int,
                             storage_type: str,
                             warehouse_id: int,
                             available_places: int) -> Optional[StoragePlaceSchema]:
        query = text("""
            INSERT INTO storage_places (storage_type, warehouse_id, available_places)
            VALUES (:storage_type, :warehouse_id, :available_places)
            RETURNING id, storage_type, warehouse_id, available_places;
        """)
        result = await session.execute(query, {
            "storage_type": storage_type,
            "warehouse_id": warehouse_id,
            "available_places": available_places})
        row = result.mappings().first()
        return StoragePlaceSchema.model_validate(dict(row)) if row else None



    async def update_storage_place_by_id(self, session: AsyncSession,
                             id_storage_place: int,
                             storage_type: str,
                             warehouse_id: int,
                             available_places: int) -> Optional[StoragePlaceSchema]:
        query = text("""
            UPDATE storage_places
            SET storage_type = :storage_type, warehouse_id = :warehouse_id, available_places = :available_places
            WHERE id = :id
            RETURNING id, storage_type, warehouse_id, available_places;
        """)
        result = await session.execute(query, {
            "id": id_storage_place,
            "storage_type": storage_type,
            "warehouse_id": warehouse_id,
            "available_places": available_places})
        row = result.mappings().first()
        return StoragePlaceSchema.model_validate(dict(row)) if row else None

    async def delete_storage_place_by_id(self, session: AsyncSession, id_storage_place: int) -> bool:
        query = text("DELETE FROM storage_places WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_storage_place})
        row = result.fetchone()
        return row is not None