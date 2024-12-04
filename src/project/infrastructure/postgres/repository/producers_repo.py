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
        session: AsyncSession,
    ) -> list[ProducerSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.producers;"

        producers = await session.execute(text(query))

        return [ProducerSchema.model_validate(obj=producer) for producer in producers.mappings().all()]