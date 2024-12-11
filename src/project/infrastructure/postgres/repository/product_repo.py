from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.infrastructure.postgres.models import Product
from project.schemas.Product import ProductSchema
from project.core.config import settings


class ProductRepository:
    _collection: Type[Product] = Product

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_products(self, session: AsyncSession) -> list[ProductSchema]:
        query = text("SELECT * FROM products;")
        result = await session.execute(query)
        return [ProductSchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_product_by_id(self, session: AsyncSession, id_product_group: int) -> Optional[ProductSchema]:
        query = text("SELECT * FROM products WHERE id = :id;")
        result = await session.execute(query, {"id": id_product_group})
        row = result.mappings().first()
        return ProductSchema.model_validate(dict(row)) if row else None

    async def insert_product(self, session: AsyncSession,
                             id: int,
                             name: str,
                             article:int,
                             unit:str,
                             product_group_id:int,
                             producer_id:int) -> Optional[ProductSchema]:
        query = text("""
            INSERT INTO products (name, article, unit, product_group_id, producer_id)
            VALUES (:name, :article, :unit, :product_group_id, :producer_id)
            RETURNING id, name, article, unit, product_group_id, producer_id;
        """)
        result = await session.execute(query, {
            "name": name,
            "article": article,
            "unit": unit,
            "product_group_id": product_group_id,
            "producer_id": producer_id})
        row = result.mappings().first()
        return ProductSchema.model_validate(dict(row)) if row else None



    async def update_product_by_id(self, session: AsyncSession,
                             id_product: int,
                             name: str,
                             article:int,
                             unit:str,
                             product_group_id:int,
                             producer_id:int) -> Optional[ProductSchema]:
        query = text("""
            UPDATE products
            SET name = :name, article = :article, unit = :unit, product_group_id = :product_group_id, producer_id = :producer_id
            WHERE id = :id
            RETURNING id, name, article, unit, product_group_id, producer_id;
        """)
        result = await session.execute(query, {
            "id": id_product,
            "name": name,
            "article": article,
            "unit": unit,
            "product_group_id": product_group_id,
            "producer_id": producer_id})
        row = result.mappings().first()
        return ProductSchema.model_validate(dict(row)) if row else None

    async def delete_product_group_by_id(self, session: AsyncSession, id_product: int) -> bool:
        query = text("DELETE FROM products WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_product})
        row = result.fetchone()
        return row is not None
