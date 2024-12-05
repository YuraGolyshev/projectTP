from fastapi import APIRouter, HTTPException
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.client import ClientSchema
from project.infrastructure.postgres.repository.client_repo import ClientRepository
from project.infrastructure.postgres.repository.producers_repo import ProducerRepository # Импорт репозитория
from project.schemas.Producer import ProducerSchema # Импорт схемы


router = APIRouter()


@router.get("/all_clients", response_model=list[ClientSchema])
async def get_all_clients() -> list[ClientSchema]:
    client_repo = ClientRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await client_repo.check_connection(session=session)
        all_clients = await client_repo.get_all_clients(session=session)

    return all_clients

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