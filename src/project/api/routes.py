from fastapi import APIRouter, HTTPException
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.client import ClientSchema
from project.infrastructure.postgres.repository.client_repo import ClientRepository
from project.infrastructure.postgres.repository.producers_repo import ProducerRepository
from project.schemas.Producer import ProducerSchema
from project.infrastructure.postgres.repository.product_groups_repo import ProductGroupRepository
from project.schemas.ProductGroup import ProductGroupSchema
from project.infrastructure.postgres.repository.product_repo import ProductRepository
from project.schemas.Product import ProductSchema
from project.schemas.movement import MovementSchema
from project.infrastructure.postgres.repository.movement_repo import MovementRepository
from project.schemas.delivery import DeliverySchema
from project.infrastructure.postgres.repository.delivery_repo import DeliveryRepository
from project.schemas.delivery_detail import DeliveryDetailSchema
from project.infrastructure.postgres.repository.delivery_detail_repo import DeliveryDetailRepository
from project.schemas.shipment import ShipmentSchema
from project.infrastructure.postgres.repository.shipment_repo import ShipmentRepository
from project.schemas.shipment_detail import ShipmentDetailSchema
from project.infrastructure.postgres.repository.shipment_detail_repo import ShipmentDetailRepository
from project.schemas.products_in_warehouse import ProductsInWarehouseSchema
from project.infrastructure.postgres.repository.products_in_warehouse_repo import ProductsInWarehouseRepository
from project.schemas.warehouse import WarehouseSchema
from project.infrastructure.postgres.repository.warehouse_repo import WarehouseRepository
from project.schemas.supplier import SupplierSchema
from project.infrastructure.postgres.repository.supplier_repo import SupplierRepository
from project.schemas.storage_place import StoragePlaceSchema
from project.infrastructure.postgres.repository.storage_place_repo import StoragePlaceRepository
from project.infrastructure.postgres.repository.users_repo import UsersRepository
from project.schemas.user import UserSchema
from project.schemas.login import LoginSchema
from project.schemas.register import RegisterSchema
router = APIRouter()

# Registration of User
@router.post("/register", response_model=UserSchema)
async def register(user: RegisterSchema) -> UserSchema:
    users_repo = UsersRepository()
    database = PostgresDatabase()

    if user.role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="role can be only 'user' or 'admin'")
    async with database.session() as session:
        await users_repo.check_connection(session=session)
        new_user = await users_repo.register_user(session=session,
                                                  name=user.name,
                                                  email=user.email,
                                                  password=user.password,
                                                  role=user.role)
    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to register user")
    return new_user

@router.post("/login", response_model=UserSchema)
async def login(user: LoginSchema) -> UserSchema:
    users_repo = UsersRepository()
    database = PostgresDatabase()
    async with database.session() as session:
        await users_repo.check_connection(session=session)
        find_user = await users_repo.login_user(session=session, email=user.email, password=user.password)
    if not find_user:
        raise HTTPException(status_code=400, detail="User is not found")
    return find_user
# other Users CRUD
@router.get("/all_users", response_model=list[UserSchema])
async def get_all_users() -> list[UserSchema]:
    users_repo = UsersRepository()
    database = PostgresDatabase()
    async with database.session() as session:
        await users_repo.check_connection(session=session)
        all_users = await users_repo.get_all_users(session=session)
    return all_users
@router.get("/user/{id}", response_model=UserSchema)
async def get_user_by_id(id: int) -> UserSchema:
    users_repo = UsersRepository()
    database = PostgresDatabase()
    async with database.session() as session:
        await users_repo.check_connection(session=session)
        user = await users_repo.get_user_by_id(session=session, id_user=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# CLIENT ROUTES
@router.get("/clients", response_model=list[ClientSchema])
async def get_all_clients() -> list[ClientSchema]:
    client_repo = ClientRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await client_repo.check_connection(session=session)
        all_clients = await client_repo.get_all_clients(session=session)

    return all_clients


@router.get("/clients/{id}", response_model=ClientSchema)
async def get_client_by_id(id: int) -> ClientSchema:
    client_repo = ClientRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await client_repo.check_connection(session=session)
        client = await client_repo.get_client_by_id(session=session, id_client=id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client


@router.post("/clients", response_model=ClientSchema)
async def insert_client(client: ClientSchema) -> ClientSchema:
    client_repo = ClientRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await client_repo.check_connection(session=session)
        new_client = await client_repo.insert_client(session=session, **client.dict())

    if not new_client:
        raise HTTPException(status_code=500, detail="Failed to insert client")

    return new_client


@router.put("/clients/{id}", response_model=ClientSchema)
async def update_client_by_id(id: int, client: ClientSchema) -> ClientSchema:
    client_repo = ClientRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await client_repo.check_connection(session=session)
        updated_client = await client_repo.update_client_by_id(
            session=session,
            id_client=id,
            name=client.name,
            email=client.email,
            password=client.password,
            phone_number=client.phone_number)

    if not updated_client:
        raise HTTPException(status_code=404, detail="Client not found or failed to update")

    return updated_client


@router.delete("/clients/{id}", response_model=dict)
async def delete_client_by_id(id: int) -> dict:
    client_repo = ClientRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await client_repo.check_connection(session=session)
        deleted = await client_repo.delete_client_by_id(session=session, id_client=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Client not found or failed to delete")

    return {"message": "Client deleted successfully"}

@router.get("/all_producers", response_model=list[ProducerSchema])
async def get_all_producers() -> list[ProducerSchema]:
    producer_repo = ProducerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await producer_repo.check_connection(session=session)
        all_producers = await producer_repo.get_all_producers(session=session)

    return all_producers


@router.get("/producer/{id}", response_model=ProducerSchema)
async def get_producer_by_id(id: int) -> ProducerSchema:
    producer_repo = ProducerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await producer_repo.check_connection(session=session)
        producer = await producer_repo.get_producer_by_id(session=session, id_producer=id)

    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")

    return producer


@router.post("/producer", response_model=ProducerSchema)
async def insert_producer(producer: ProducerSchema) -> ProducerSchema:
    producer_repo = ProducerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await producer_repo.check_connection(session=session)
        new_producer = await producer_repo.insert_producer(session=session, **producer.dict())

    if not new_producer:
        raise HTTPException(status_code=500, detail="Failed to insert producer")

    return new_producer


@router.put("/producer/{id}", response_model=ProducerSchema)
async def update_producer(id: int, producer: ProducerSchema) -> ProducerSchema:
    producer_repo = ProducerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await producer_repo.check_connection(session=session)
        updated_producer = await producer_repo.update_producer_by_id(session=session, id_producer=id, name=producer.name)

    if not updated_producer:
        raise HTTPException(status_code=404, detail="Producer not found or failed to update")

    return updated_producer


@router.delete("/producer/{id}", response_model=dict)
async def delete_producer(id: int) -> dict:
    producer_repo = ProducerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await producer_repo.check_connection(session=session)
        deleted = await producer_repo.delete_producer_by_id(session=session, id_producer=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Producer not found or failed to delete")

    return {"message": "Producer deleted successfully"}

@router.get("/all_product_groups", response_model=list[ProductGroupSchema])
async def get_all_product_groups() -> list[ProductGroupSchema]:
    product_groups_repo = ProductGroupRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_groups_repo.check_connection(session=session)
        all_product_groups = await product_groups_repo.get_all_product_groups(session=session)

    return all_product_groups


@router.get("/product_groups/{id}", response_model=ProductGroupSchema)
async def get_product_group_by_id(id: int) -> ProductGroupSchema:
    product_groups_repo = ProductGroupRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_groups_repo.check_connection(session=session)
        product_group = await product_groups_repo.get_product_group_by_id(session=session, id_product_group=id)

    if not product_group:
        raise HTTPException(status_code=404, detail="Product group not found")

    return product_group


@router.post("/product_groups", response_model=ProductGroupSchema)
async def insert_product_group(product_group: ProductGroupSchema) -> ProductGroupSchema:
    product_groups_repo = ProductGroupRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_groups_repo.check_connection(session=session)
        new_product_group = await product_groups_repo.insert_product_group(session=session, **product_group.dict())

    if not new_product_group:
        raise HTTPException(status_code=500, detail="Failed to insert product group")

    return new_product_group


@router.put("/product_groups/{id}", response_model=ProductGroupSchema)
async def update_product_group_by_id(id: int, product_group: ProductGroupSchema) -> ProductGroupSchema:
    product_groups_repo = ProductGroupRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_groups_repo.check_connection(session=session)
        updated_product_group = await product_groups_repo.update_product_group_by_id(session=session, id_product_group=id, name=product_group.name)

    if not updated_product_group:
        raise HTTPException(status_code=404, detail="Product group not found or failed to update")

    return updated_product_group


@router.delete("/product_groups/{id}", response_model=dict)
async def delete_product_group_by_id(id: int) -> dict:
    product_groups_repo = ProductGroupRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_groups_repo.check_connection(session=session)
        deleted = await product_groups_repo.delete_product_group_by_id(session=session, id_product_group=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product group not found or failed to delete")

    return {"message": "Product group deleted successfully"}

@router.get("/all_products", response_model=list[ProductSchema])
async def get_all_products() -> list[ProductSchema]:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        all_products = await product_repo.get_all_products(session=session)

    return all_products


@router.get("/product/{id}", response_model=ProductSchema)
async def get_product_by_id(id: int) -> ProductSchema:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        product = await product_repo.get_product_by_id(session=session, id_product=id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/product", response_model=ProductSchema)
async def insert_product(product: ProductSchema) -> ProductSchema:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        new_product = await product_repo.insert_product(session=session, **product.dict())

    if not new_product:
        raise HTTPException(status_code=500, detail="Failed to insert product")

    return new_product


@router.put("/product/{id}", response_model=ProductSchema)
async def update_product_by_id(id: int, product: ProductSchema) -> ProductSchema:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        updated_product = await product_repo.update_product_by_id(
            session=session,
            id_product_group=id,
            name=product.name,
            article=product.article,
            product_group_id=product.product_group_id,
            producer_id=product.producer_id)

    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found or failed to update")

    return updated_product


@router.delete("/product/{id}", response_model=dict)
async def delete_product_by_id(id: int) -> dict:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        deleted = await product_repo.delete_product_by_id(session=session, id_product=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found or failed to delete")

    return {"message": "Product deleted successfully"}
# WAREHOUSE ROUTES

@router.get("/warehouses", response_model=list[WarehouseSchema])
async def get_all_warehouses() -> list[WarehouseSchema]:
    warehouse_repo = WarehouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await warehouse_repo.check_connection(session=session)
        all_warehouses = await warehouse_repo.get_all_warehouses(session=session)

    return all_warehouses


@router.get("/warehouses/{id}", response_model=WarehouseSchema)
async def get_warehouse_by_id(id: int) -> WarehouseSchema:
    warehouse_repo = WarehouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await warehouse_repo.check_connection(session=session)
        warehouse = await warehouse_repo.get_warehouse_by_id(session=session, id_warehouse=id)

    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    return warehouse


@router.post("/warehouses", response_model=WarehouseSchema)
async def insert_warehouse(warehouse: WarehouseSchema) -> WarehouseSchema:
    warehouse_repo = WarehouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await warehouse_repo.check_connection(session=session)
        new_warehouse = await warehouse_repo.insert_warehouse(session=session, **warehouse.dict())

    if not new_warehouse:
        raise HTTPException(status_code=500, detail="Failed to insert warehouse")

    return new_warehouse


@router.put("/warehouses/{id}", response_model=WarehouseSchema)
async def update_warehouse_by_id(id: int, warehouse: WarehouseSchema) -> WarehouseSchema:
    warehouse_repo = WarehouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await warehouse_repo.check_connection(session=session)
        updated_warehouse = await warehouse_repo.update_warehouse_by_id(
            session=session,
            id_warehouse=id,
            available_types=warehouse.available_types,
            address=warehouse.address,
            name=warehouse.name,
            available_places=warehouse.available_places)

    if not updated_warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found or failed to update")

    return updated_warehouse


@router.delete("/warehouses/{id}", response_model=dict)
async def delete_warehouse_by_id(id: int) -> dict:
    warehouse_repo = WarehouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await warehouse_repo.check_connection(session=session)
        deleted = await warehouse_repo.delete_warehouse_by_id(session=session, id_warehouse=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Warehouse not found or failed to delete")

    return {"message": "Warehouse deleted successfully"}



# SUPPLIER ROUTES

@router.get("/suppliers", response_model=list[SupplierSchema])
async def get_all_suppliers() -> list[SupplierSchema]:
    supplier_repo = SupplierRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await supplier_repo.check_connection(session=session)
        all_suppliers = await supplier_repo.get_all_suppliers(session=session)

    return all_suppliers


@router.get("/suppliers/{id}", response_model=SupplierSchema)
async def get_supplier_by_id(id: int) -> SupplierSchema:
    supplier_repo = SupplierRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await supplier_repo.check_connection(session=session)
        supplier = await supplier_repo.get_supplier_by_id(session=session, id_supplier=id)

    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return supplier


@router.post("/suppliers", response_model=SupplierSchema)
async def insert_supplier(supplier: SupplierSchema) -> SupplierSchema:
    supplier_repo = SupplierRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await supplier_repo.check_connection(session=session)
        new_supplier = await supplier_repo.insert_supplier(session=session, **supplier.dict())

    if not new_supplier:
        raise HTTPException(status_code=500, detail="Failed to insert supplier")

    return new_supplier


@router.put("/suppliers/{id}", response_model=SupplierSchema)
async def update_supplier_by_id(id: int, supplier: SupplierSchema) -> SupplierSchema:
    supplier_repo = SupplierRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await supplier_repo.check_connection(session=session)
        updated_supplier = await supplier_repo.update_supplier_by_id(session=session, id_supplier=id, name=supplier.name)

    if not updated_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found or failed to update")

    return updated_supplier


@router.delete("/suppliers/{id}", response_model=dict)
async def delete_supplier_by_id(id: int) -> dict:
    supplier_repo = SupplierRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await supplier_repo.check_connection(session=session)
        deleted = await supplier_repo.delete_supplier_by_id(session=session, id_supplier=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Supplier not found or failed to delete")

    return {"message": "Supplier deleted successfully"}



# STORAGE PLACE ROUTES

@router.get("/storage_places", response_model=list[StoragePlaceSchema])
async def get_all_storage_places() -> list[StoragePlaceSchema]:
    storage_place_repo = StoragePlaceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await storage_place_repo.check_connection(session=session)
        all_storage_places = await storage_place_repo.get_all_storage_places(session=session)

    return all_storage_places


@router.get("/storage_places/{id}", response_model=StoragePlaceSchema)
async def get_storage_place_by_id(id: int) -> StoragePlaceSchema:
    storage_place_repo = StoragePlaceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await storage_place_repo.check_connection(session=session)
        storage_place = await storage_place_repo.get_storage_place_by_id(session=session, id_storage_place=id)

    if not storage_place:
        raise HTTPException(status_code=404, detail="Storage place not found")

    return storage_place


@router.post("/storage_places", response_model=StoragePlaceSchema)
async def insert_storage_place(storage_place: StoragePlaceSchema) -> StoragePlaceSchema:
    storage_place_repo = StoragePlaceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await storage_place_repo.check_connection(session=session)
        new_storage_place = await storage_place_repo.insert_storage_place(session=session, **storage_place.dict())

    if not new_storage_place:
        raise HTTPException(status_code=500, detail="Failed to insert storage place")

    return new_storage_place


@router.put("/storage_places/{id}", response_model=StoragePlaceSchema)
async def update_storage_place_by_id(id: int, storage_place: StoragePlaceSchema) -> StoragePlaceSchema:
    storage_place_repo = StoragePlaceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await storage_place_repo.check_connection(session=session)
        updated_storage_place = await storage_place_repo.update_storage_place_by_id(
            session=session,
            id_storage_place=id,
            storage_type=storage_place.storage_type,
            warehouse_id=storage_place.warehouse_id,
            available_places=storage_place.available_places)

    if not updated_storage_place:
        raise HTTPException(status_code=404, detail="Storage place not found or failed to update")

    return updated_storage_place


@router.delete("/storage_places/{id}", response_model=dict)
async def delete_storage_place_by_id(id: int) -> dict:
    storage_place_repo = StoragePlaceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await storage_place_repo.check_connection(session=session)
        deleted = await storage_place_repo.delete_storage_place_by_id(session=session, id_storage_place=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Storage place not found or failed to delete")

    return {"message": "Storage place deleted successfully"}

# SHIPMENT ROUTES

@router.get("/shipments", response_model=list[ShipmentSchema])
async def get_all_shipments() -> list[ShipmentSchema]:
    shipment_repo = ShipmentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await shipment_repo.check_connection(session=session)
        all_shipments = await shipment_repo.get_all_shipments(session=session)

    return all_shipments


@router.get("/shipments/{id}", response_model=ShipmentSchema)
async def get_shipment_by_id(id: int) -> ShipmentSchema:
    shipment_repo = ShipmentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await shipment_repo.check_connection(session=session)
        shipment = await shipment_repo.get_shipment_by_id(session=session, id_shipment=id)

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return shipment


@router.post("/shipments", response_model=ShipmentSchema)
async def insert_shipment(shipment: ShipmentSchema) -> ShipmentSchema:
    shipment_repo = ShipmentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await shipment_repo.check_connection(session=session)
        new_shipment = await shipment_repo.insert_shipment(session=session, **shipment.dict())

    if not new_shipment:
        raise HTTPException(status_code=500, detail="Failed to insert shipment")

    return new_shipment


@router.put("/shipments/{id}", response_model=ShipmentSchema)
async def update_shipment_by_id(id: int, shipment: ShipmentSchema) -> ShipmentSchema:
    shipment_repo = ShipmentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await shipment_repo.check_connection(session=session)
        updated_shipment = await shipment_repo.update_shipment_by_id(
            session=session,
            id_shipment=id,
            address=shipment.address,
            total_sum=shipment.total_sum,
            warehouse_id=shipment.warehouse_id,
            client_id=shipment.client_id,
            shipment_date=shipment.shipment_date)

    if not updated_shipment:
        raise HTTPException(status_code=404, detail="Shipment not found or failed to update")

    return updated_shipment


@router.delete("/shipments/{id}", response_model=dict)
async def delete_shipment_by_id(id: int) -> dict:
    shipment_repo = ShipmentRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await shipment_repo.check_connection(session=session)
        deleted = await shipment_repo.delete_shipment_by_id(session=session, id_shipment=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Shipment not found or failed to delete")

    return {"message": "Shipment deleted successfully"}



# SHIPMENT DETAIL ROUTES

@router.get("/shipment_details", response_model=list[ShipmentDetailSchema])
async def get_all_shipment_details() -> list[ShipmentDetailSchema]:
    shipment_detail_repo = ShipmentDetailRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await shipment_detail_repo.check_connection(session=session)
        all_shipment_details = await shipment_detail_repo.get_all_shipment_details(session=session)

    return all_shipment_details


@router.get("/shipment_details/{id}", response_model=ShipmentDetailSchema)
async def get_shipment_detail_by_id(id: int) -> ShipmentDetailSchema:
    shipment_detail_repo = ShipmentDetailRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await shipment_detail_repo.check_connection(session=session)
        shipment_detail = await shipment_detail_repo.get_shipment_detail_by_id(session=session, id_shipment_detail=id)

    if not shipment_detail:
        raise HTTPException(status_code=404, detail="Shipment detail not found")

    return shipment_detail


@router.post("/shipment_details", response_model=ShipmentDetailSchema)
async def insert_shipment_detail(shipment_detail: ShipmentDetailSchema) -> ShipmentDetailSchema:
    shipment_detail_repo = ShipmentDetailRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await shipment_detail_repo.check_connection(session=session)
        new_shipment_detail = await shipment_detail_repo.insert_shipment_detail(session=session, **shipment_detail.dict())

    if not new_shipment_detail:
        raise HTTPException(status_code=500, detail="Failed to insert shipment detail")

    return new_shipment_detail


@router.put("/shipment_details/{id}", response_model=ShipmentDetailSchema)
async def update_shipment_detail_by_id(id: int, shipment_detail: ShipmentDetailSchema) -> ShipmentDetailSchema:
    shipment_detail_repo = ShipmentDetailRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await shipment_detail_repo.check_connection(session=session)
        updated_shipment_detail = await shipment_detail_repo.update_shipment_detail_by_id(
            session=session,
            id_shipment_detail=id,
            shipment_id=shipment_detail.shipment_id,
            product_id=shipment_detail.product_id,
            quantity=shipment_detail.quantity,
            price=shipment_detail.price)

    if not updated_shipment_detail:
        raise HTTPException(status_code=404, detail="Shipment detail not found or failed to update")

    return updated_shipment_detail


@router.delete("/shipment_details/{id}", response_model=dict)
async def delete_shipment_detail_by_id(id: int) -> dict:
    shipment_detail_repo = ShipmentDetailRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await shipment_detail_repo.check_connection(session=session)
        deleted = await shipment_detail_repo.delete_shipment_detail_by_id(session=session, id_shipment_detail=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Shipment detail not found or failed to delete")

    return {"message": "Shipment detail deleted successfully"}



# PRODUCTS IN WAREHOUSE ROUTES

@router.get("/products_in_warehouses", response_model=list[ProductsInWarehouseSchema])
async def get_all_products_in_warehouses() -> list[ProductsInWarehouseSchema]:
    products_in_warehouse_repo = ProductsInWarehouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await products_in_warehouse_repo.check_connection(session=session)
        all_products_in_warehouses = await products_in_warehouse_repo.get_all_products_in_warehouses(session=session)

    return all_products_in_warehouses


@router.get("/products_in_warehouses/{id}", response_model=ProductsInWarehouseSchema)
async def get_products_in_warehouse_by_id(id: int) -> ProductsInWarehouseSchema:
    products_in_warehouse_repo = ProductsInWarehouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await products_in_warehouse_repo.check_connection(session=session)
        products_in_warehouse = await products_in_warehouse_repo.get_products_in_warehouse_by_id(session=session, id_products_in_warehouse=id)

    if not products_in_warehouse:
        raise HTTPException(status_code=404, detail="Products in warehouse not found")

    return products_in_warehouse


@router.post("/products_in_warehouses", response_model=ProductsInWarehouseSchema)
async def insert_products_in_warehouse(products_in_warehouse: ProductsInWarehouseSchema) -> ProductsInWarehouseSchema:
    products_in_warehouse_repo = ProductsInWarehouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await products_in_warehouse_repo.check_connection(session=session)
        new_products_in_warehouse = await products_in_warehouse_repo.insert_products_in_warehouse(session=session, **products_in_warehouse.dict())

    if not new_products_in_warehouse:
        raise HTTPException(status_code=500, detail="Failed to insert products in warehouse")

    return new_products_in_warehouse


@router.put("/products_in_warehouses/{id}", response_model=ProductsInWarehouseSchema)
async def update_products_in_warehouse_by_id(id: int, products_in_warehouse: ProductsInWarehouseSchema) -> ProductsInWarehouseSchema:
    products_in_warehouse_repo = ProductsInWarehouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await products_in_warehouse_repo.check_connection(session=session)
        updated_products_in_warehouse = await products_in_warehouse_repo.update_products_in_warehouse_by_id(
            session=session,
            id_products_in_warehouse=id,
            warehouse_id=products_in_warehouse.warehouse_id,
            product_id=products_in_warehouse.product_id,
            quantity=products_in_warehouse.quantity,
            storage_place_id=products_in_warehouse.storage_place_id,
            place_number=products_in_warehouse.place_number)

    if not updated_products_in_warehouse:
        raise HTTPException(status_code=404, detail="Products in warehouse not found or failed to update")

    return updated_products_in_warehouse


@router.delete("/products_in_warehouses/{id}", response_model=dict)
async def delete_products_in_warehouse_by_id(id: int) -> dict:
    products_in_warehouse_repo = ProductsInWarehouseRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await products_in_warehouse_repo.check_connection(session=session)
        deleted = await products_in_warehouse_repo.delete_products_in_warehouse_by_id(session=session, id_products_in_warehouse=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Products in warehouse not found or failed to delete")

    return {"message": "Products in warehouse deleted successfully"}

# MOVEMENT ROUTES

@router.get("/movements", response_model=list[MovementSchema])
async def get_all_movements() -> list[MovementSchema]:
    movement_repo = MovementRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await movement_repo.check_connection(session=session)
        all_movements = await movement_repo.get_all_movements(session=session)

    return all_movements


@router.get("/movements/{id}", response_model=MovementSchema)
async def get_movement_by_id(id: int) -> MovementSchema:
    movement_repo = MovementRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await movement_repo.check_connection(session=session)
        movement = await movement_repo.get_movement_by_id(session=session, id_movement=id)

    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")

    return movement


@router.post("/movements", response_model=MovementSchema)
async def insert_movement(movement: MovementSchema) -> MovementSchema:
    movement_repo = MovementRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await movement_repo.check_connection(session=session)
        new_movement = await movement_repo.insert_movement(session=session, **movement.dict())

    if not new_movement:
        raise HTTPException(status_code=500, detail="Failed to insert movement")

    return new_movement


@router.put("/movements/{id}", response_model=MovementSchema)
async def update_movement_by_id(id: int, movement: MovementSchema) -> MovementSchema:
    movement_repo = MovementRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await movement_repo.check_connection(session=session)
        updated_movement = await movement_repo.update_movement_by_id(
            session=session,
            id_movement=id,
            product_id=movement.product_id,
            quantity=movement.quantity,
            from_storage_place_id=movement.from_storage_place_id,
            to_storage_place_id=movement.to_storage_place_id,
            movement_date=movement.movement_date)

    if not updated_movement:
        raise HTTPException(status_code=404, detail="Movement not found or failed to update")

    return updated_movement


@router.delete("/movements/{id}", response_model=dict)
async def delete_movement_by_id(id: int) -> dict:
    movement_repo = MovementRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await movement_repo.check_connection(session=session)
        deleted = await movement_repo.delete_movement_by_id(session=session, id_movement=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Movement not found or failed to delete")

    return {"message": "Movement deleted successfully"}



# DELIVERY ROUTES

@router.get("/deliveries", response_model=list[DeliverySchema])
async def get_all_deliveries() -> list[DeliverySchema]:
    delivery_repo = DeliveryRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await delivery_repo.check_connection(session=session)
        all_deliveries = await delivery_repo.get_all_deliveries(session=session)

    return all_deliveries


@router.get("/deliveries/{id}", response_model=DeliverySchema)
async def get_delivery_by_id(id: int) -> DeliverySchema:
    delivery_repo = DeliveryRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await delivery_repo.check_connection(session=session)
        delivery = await delivery_repo.get_delivery_by_id(session=session, id_delivery=id)

    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return delivery


@router.post("/deliveries", response_model=DeliverySchema)
async def insert_delivery(delivery: DeliverySchema) -> DeliverySchema:
    delivery_repo = DeliveryRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await delivery_repo.check_connection(session=session)
        new_delivery = await delivery_repo.insert_delivery(session=session, **delivery.dict())

    if not new_delivery:
        raise HTTPException(status_code=500, detail="Failed to insert delivery")

    return new_delivery


@router.put("/deliveries/{id}", response_model=DeliverySchema)
async def update_delivery_by_id(id: int, delivery: DeliverySchema) -> DeliverySchema:
    delivery_repo = DeliveryRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await delivery_repo.check_connection(session=session)
        updated_delivery = await delivery_repo.update_delivery_by_id(
            session=session,
            id_delivery=id,
            total_sum=delivery.total_sum,
            supplier_id=delivery.supplier_id,
            delivery_date=delivery.delivery_date)

    if not updated_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found or failed to update")

    return updated_delivery


@router.delete("/deliveries/{id}", response_model=dict)
async def delete_delivery_by_id(id: int) -> dict:
    delivery_repo = DeliveryRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await delivery_repo.check_connection(session=session)
        deleted = await delivery_repo.delete_delivery_by_id(session=session, id_delivery=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery not found or failed to delete")

    return {"message": "Delivery deleted successfully"}



# DELIVERY DETAIL ROUTES

@router.get("/delivery_details", response_model=list[DeliveryDetailSchema])
async def get_all_delivery_details() -> list[DeliveryDetailSchema]:
    delivery_detail_repo = DeliveryDetailRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await delivery_detail_repo.check_connection(session=session)
        all_delivery_details = await delivery_detail_repo.get_all_delivery_details(session=session)

    return all_delivery_details


@router.get("/delivery_details/{id}", response_model=DeliveryDetailSchema)
async def get_delivery_detail_by_id(id: int) -> DeliveryDetailSchema:
    delivery_detail_repo = DeliveryDetailRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await delivery_detail_repo.check_connection(session=session)
        delivery_detail = await delivery_detail_repo.get_delivery_detail_by_id(session=session, id_delivery_detail=id)

    if not delivery_detail:
        raise HTTPException(status_code=404, detail="Delivery detail not found")

    return delivery_detail


@router.post("/delivery_details", response_model=DeliveryDetailSchema)
async def insert_delivery_detail(delivery_detail: DeliveryDetailSchema) -> DeliveryDetailSchema:
    delivery_detail_repo = DeliveryDetailRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await delivery_detail_repo.check_connection(session=session)
        new_delivery_detail = await delivery_detail_repo.insert_delivery_detail(session=session, **delivery_detail.dict())

    if not new_delivery_detail:
        raise HTTPException(status_code=500, detail="Failed to insert delivery detail")

    return new_delivery_detail


@router.put("/delivery_details/{id}", response_model=DeliveryDetailSchema)
async def update_delivery_detail_by_id(id: int, delivery_detail: DeliveryDetailSchema) -> DeliveryDetailSchema:
    delivery_detail_repo = DeliveryDetailRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await delivery_detail_repo.check_connection(session=session)
        updated_delivery_detail = await delivery_detail_repo.update_delivery_detail_by_id(
            session=session,
            id_delivery_detail=id,
            delivery_id=delivery_detail.delivery_id,
            product_id=delivery_detail.product_id,
            quantity=delivery_detail.quantity,
            price=delivery_detail.price)

    if not updated_delivery_detail:
        raise HTTPException(status_code=404, detail="Delivery detail not found or failed to update")

    return updated_delivery_detail


@router.delete("/delivery_details/{id}", response_model=dict)
async def delete_delivery_detail_by_id(id: int) -> dict:
    delivery_detail_repo = DeliveryDetailRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await delivery_detail_repo.check_connection(session=session)
        deleted = await delivery_detail_repo.delete_delivery_detail_by_id(session=session, id_delivery_detail=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery detail not found or failed to delete")

    return {"message": "Delivery detail deleted successfully"}