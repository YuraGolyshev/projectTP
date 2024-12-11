from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.infrastructure.postgres.models import ProductsInWarehouse
from project.schemas.products_in_warehouse import ProductsInWarehouseSchema
from project.core.config import settings


class ProductsInWarehouseRepository:
    _collection: Type[ProductsInWarehouse] = ProductsInWarehouse

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_products_in_warehouses(self, session: AsyncSession) -> list[ProductsInWarehouseSchema]:
        query = text("SELECT * FROM products_in_warehouse;")
        result = await session.execute(query)
        return [ProductsInWarehouseSchema.model_validate(dict(row)) for row in result.mappings().all()]

    async def get_products_in_warehouse_by_id(self, session: AsyncSession, id_products_in_warehouse: int) -> Optional[ProductsInWarehouseSchema]:
        query = text("SELECT * FROM products_in_warehouse WHERE id = :id;")
        result = await session.execute(query, {"id": id_products_in_warehouse})
        row = result.mappings().first()
        return ProductsInWarehouseSchema.model_validate(dict(row)) if row else None

    async def insert_products_in_warehouse(self, session: AsyncSession,
                             id: int,
                             warehouse_id: int,
                             product_id: int,
                             quantity: int,
                             storage_place_id: int,
                             place_number: int) -> Optional[ProductsInWarehouseSchema]:
        query = text("""
            INSERT INTO products_in_warehouse (warehouse_id, product_id, quantity, storage_place_id, place_number)
            VALUES (:warehouse_id, :product_id, :quantity, :storage_place_id, :place_number)
            RETURNING id, warehouse_id, product_id, quantity, storage_place_id, place_number;
        """)
        result = await session.execute(query, {
            "warehouse_id": warehouse_id,
            "product_id": product_id,
            "quantity": quantity,
            "storage_place_id": storage_place_id,
            "place_number": place_number})
        row = result.mappings().first()
        return ProductsInWarehouseSchema.model_validate(dict(row)) if row else None



    async def update_products_in_warehouse_by_id(self, session: AsyncSession,
                             id_products_in_warehouse: int,
                             warehouse_id: int,
                             product_id: int,
                             quantity: int,
                             storage_place_id: int,
                             place_number: int) -> Optional[ProductsInWarehouseSchema]:
        query = text("""
            UPDATE products_in_warehouse
            SET warehouse_id = :warehouse_id, product_id = :product_id, quantity = :quantity, storage_place_id = :storage_place_id, place_number = :place_number
            WHERE id = :id
            RETURNING id, warehouse_id, product_id, quantity, storage_place_id, place_number;
        """)
        result = await session.execute(query, {
            "id": id_products_in_warehouse,
            "warehouse_id": warehouse_id,
            "product_id": product_id,
            "quantity": quantity,
            "storage_place_id": storage_place_id,
            "place_number": place_number})
        row = result.mappings().first()
        return ProductsInWarehouseSchema.model_validate(dict(row)) if row else None

    async def delete_products_in_warehouse_by_id(self, session: AsyncSession, id_products_in_warehouse: int) -> bool:
        query = text("DELETE FROM products_in_warehouse WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_products_in_warehouse})
        row = result.fetchone()
        return row is not None