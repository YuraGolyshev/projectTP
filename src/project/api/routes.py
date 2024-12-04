from fastapi import APIRouter
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
