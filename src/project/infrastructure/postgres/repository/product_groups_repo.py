from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.infrastructure.postgres.models import ProductGroup
from project.schemas.ProductGroup import ProductGroupSchema
from project.core.config import settings


class ProductGroupRepository:
    _collection: Type[ProductGroup] = ProductGroup

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_product_groups(self, session: AsyncSession) -> list[ProductGroupSchema]:
        query = text("SELECT * FROM product_groups;")
        result = await session.execute(query)
        return [ProductGroupSchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_product_group_by_id(self, session: AsyncSession, id_product_group: int) -> Optional[ProductGroupSchema]:
        query = text("SELECT * FROM product_groups WHERE id = :id;")
        result = await session.execute(query, {"id": id_product_group})
        row = result.mappings().first()
        return ProductGroupSchema.model_validate(dict(row)) if row else None

    async def insert_product_group(self, session: AsyncSession, id:int, name: str) -> Optional[ProductGroupSchema]:
        query = text("""
            INSERT INTO product_groups (name)
            VALUES (:name)
            RETURNING id, name;
        """)
        result = await session.execute(query, {"name": name})
        row = result.mappings().first()
        return ProductGroupSchema.model_validate(dict(row)) if row else None



    async def update_product_group_by_id(self, session: AsyncSession, id_product_group: int, name: str) -> Optional[ProductGroupSchema]:
        query = text("""
            UPDATE product_groups
            SET name = :name
            WHERE id = :id
            RETURNING id, name;
        """)
        result = await session.execute(query, {"id": id_product_group, "name": name})
        await session.commit() # очень важно
        row = result.mappings().first()
        return ProductGroupSchema.model_validate(dict(row)) if row else None

    async def delete_product_group_by_id(self, session: AsyncSession, id_product_group: int) -> bool:
        query = text("DELETE FROM product_groups WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_product_group})
        await session.commit() # очень важно
        row = result.fetchone()
        return row is not None
