from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.client import ClientSchema
from project.infrastructure.postgres.models import Client

from project.core.config import settings


class ClientRepository:
    _collection: Type[Client] = Client

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_clients(self, session: AsyncSession) -> list[ClientSchema]:
        query = text("SELECT * FROM clients;")
        result = await session.execute(query)
        return [ClientSchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_client_by_id(self, session: AsyncSession, id_client: int) -> Optional[ClientSchema]:
        query = text("SELECT * FROM clients WHERE id = :id;")
        result = await session.execute(query, {"id": id_client})
        row = result.mappings().first()
        return ClientSchema.model_validate(dict(row)) if row else None

    async def insert_client(self, session: AsyncSession, id:int, name: str, email: str, password: str, phone_number:str) -> Optional[ClientSchema]:
        query = text("""
            INSERT INTO clients (name, email, password, phone_number)
            VALUES (:name, :email, :password, :phone_number)
            RETURNING id, name, email, password, phone_number;
        """)
        result = await session.execute(query, {
            "name": name,
            "email": email,
            "password": password,
            "phone_number": phone_number
        })
        row = result.mappings().first()
        return ClientSchema.model_validate(dict(row)) if row else None

    async def update_client_by_id(self, session: AsyncSession, id_client: int, name: str, email: str, password: str, phone_number:str) -> Optional[ClientSchema]:
        query = text("""
            UPDATE clients
            SET name = :name, email = :email, password = :password, phone_number = :phone_number
            WHERE id = :id
            RETURNING id, name, email, password, phone_number;
        """)
        result = await session.execute(query, {
            "id": id_client,
            "name": name,
            "email": email,
            "password": password,
            "phone_number": phone_number
        })
        await session.commit()
        row = result.mappings().first()
        return ClientSchema.model_validate(dict(row)) if row else None

    async def delete_client_by_id(self, session: AsyncSession, id_client: int) -> bool:
        query = text("DELETE FROM clients WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_client})
        await session.commit()
        row = result.fetchone()
        return row is not None