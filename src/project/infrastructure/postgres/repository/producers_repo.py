from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.infrastructure.postgres.models import Producer
from project.core.config import settings
from project.schemas.Producer import ProducerSchema # Импорт схемы

class ProducerRepository:
    _collection: Type[Producer] = Producer

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_producers(
            self,
            session: AsyncSession
    ) -> list[ProducerSchema]:
        query = "SELECT * FROM producers;"
        result = await session.execute(text(query))

        return [
            ProducerSchema.model_validate(dict(producer))
            for producer in result.mappings().all()
        ]

    async def get_producer_by_id(
            self,
            session: AsyncSession,
            id_producer: int
    ) -> ProducerSchema | None:
        query = text("SELECT * FROM producers WHERE id = :id")
        result = await session.execute(query, {"id": id_producer})

        producer_row = result.mappings().first()

        if producer_row:
            return ProducerSchema.model_validate(dict(producer_row))

        return None

    async def insert_producer(
            self,
            session: AsyncSession,
            id: int,
            name: str
    ) -> ProducerSchema | None:
        query = text("""
            INSERT INTO producers (name) 
                        VALUES (:name)
            RETURNING id, name
        """)

        result = await session.execute(query, {
            "name": name
        })

        producer_row = result.mappings().first()

        if producer_row:
            return ProducerSchema.model_validate(dict(producer_row))

        return None

    async def update_producer_by_id(
        self,
        session: AsyncSession,
        id_producer: int,
        name: str
    ) -> ProducerSchema | None:

        query = text(f"""
            UPDATE {settings.POSTGRES_SCHEMA}.producers 
            SET name = :name
            WHERE id = :id 
            RETURNING id, name
        """)

        result = await session.execute(query, {
            "id": id_producer,
            "name": name
        })

        updated_row = result.mappings().first()

        if updated_row:
            return ProducerSchema.model_validate(dict(updated_row))

        return None

    async def delete_producer_by_id(
        self,
        session: AsyncSession,
        id_producer: int
    ) -> bool:

        query = text("DELETE FROM producers WHERE id = :id RETURNING id")
        result = await session.execute(query, {"id": id_producer})

        deleted_row = result.fetchone()

        return deleted_row is not None