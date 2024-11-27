from fastapi import APIRouter

from project.infrastructure.postgres.repository.client_repo import ClientRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.client import ClientSchema


router = APIRouter()


@router.get("/all_clients", response_model=list[ClientSchema])
async def get_all_clients() -> list[ClientSchema]:
    client_repo = ClientRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await client_repo.check_connection(session=session)
        all_clients = await client_repo.get_all_clients(session=session)

    return all_clients
