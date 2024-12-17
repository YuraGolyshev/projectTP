from datetime import date
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.infrastructure.postgres.database import Base

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    role: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=True)


class Producer(Base):
    __tablename__ = "producers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    products = relationship("Product", back_populates="producer")

class ProductGroup(Base):
    __tablename__ = "product_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    products = relationship("Product", back_populates="product_group")

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    article: Mapped[int] = mapped_column(nullable=False)
    unit: Mapped[str] = mapped_column(nullable=False)
    product_group_id: Mapped[int] = mapped_column(ForeignKey("product_groups.id"), nullable=False)
    producer_id: Mapped[int] = mapped_column(ForeignKey("producers.id"), nullable=False)

    product_group = relationship("ProductGroup", back_populates="products")
    producer = relationship("Producer", back_populates="products")

class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(primary_key=True)
    available_types: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    available_places: Mapped[int] = mapped_column(nullable=False)
    storage_places = relationship("StoragePlace", back_populates="warehouse")
    products_in_warehouses = relationship("ProductsInWarehouse", back_populates="warehouse")
    shipments = relationship("Shipment", back_populates="warehouse")


class StoragePlace(Base):
    __tablename__ = "storage_places"

    id: Mapped[int] = mapped_column(primary_key=True)
    storage_type: Mapped[str] = mapped_column(nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    available_places: Mapped[int] = mapped_column(nullable=False)
    warehouse = relationship("Warehouse", back_populates="storage_places")
    products_in_warehouses = relationship("ProductsInWarehouse", back_populates="storage_place")
    movements = relationship("Movement", back_populates="from_storage_place", foreign_keys="[Movement.from_storage_place_id]")
    movements_to = relationship("Movement", back_populates="to_storage_place", foreign_keys="[Movement.to_storage_place_id]")



class ProductsInWarehouse(Base):
    __tablename__ = "products_in_warehouse"

    id: Mapped[int] = mapped_column(primary_key=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    storage_place_id: Mapped[int] = mapped_column(ForeignKey("storage_places.id"), nullable=False)
    place_number: Mapped[int] = mapped_column(nullable=False)

    warehouse = relationship("Warehouse", back_populates="products_in_warehouses")
    product = relationship("Product", back_populates="products_in_warehouses")
    storage_place = relationship("StoragePlace", back_populates="products_in_warehouses")


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    deliveries = relationship("Delivery", back_populates="supplier")


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(primary_key=True)
    total_sum: Mapped[float] = mapped_column(nullable=False)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False)
    delivery_date: Mapped[date] = mapped_column(nullable=False)
    supplier = relationship("Supplier", back_populates="deliveries")
    delivery_details = relationship("DeliveryDetail", back_populates="delivery")


class DeliveryDetail(Base):
    __tablename__ = "delivery_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    delivery_id: Mapped[int] = mapped_column(ForeignKey("deliveries.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    delivery = relationship("Delivery", back_populates="delivery_details")
    product = relationship("Product", back_populates="delivery_details")


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(nullable=False)
    total_sum: Mapped[float] = mapped_column(nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    shipment_date: Mapped[date] = mapped_column(nullable=False)

    warehouse = relationship("Warehouse", back_populates="shipments")
    client = relationship("Client", back_populates="shipments")
    shipment_details = relationship("ShipmentDetail", back_populates="shipment")


class ShipmentDetail(Base):
    __tablename__ = "shipment_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    shipment_id: Mapped[int] = mapped_column(ForeignKey("shipments.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    shipment = relationship("Shipment", back_populates="shipment_details")
    product = relationship("Product", back_populates="shipment_details")


class Movement(Base):
    __tablename__ = "movements"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    from_storage_place_id: Mapped[int] = mapped_column(ForeignKey("storage_places.id"), nullable=False)
    to_storage_place_id: Mapped[int] = mapped_column(ForeignKey("storage_places.id"), nullable=False)
    movement_date: Mapped[date] = mapped_column(nullable=False)

    product = relationship("Product", back_populates="movements")
    from_storage_place = relationship("StoragePlace", back_populates="movements", foreign_keys="[Movement.from_storage_place_id]")
    to_storage_place = relationship("StoragePlace", back_populates="movements_to", foreign_keys="[Movement.to_storage_place_id]")