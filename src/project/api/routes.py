from fastapi import APIRouter

from project.infrastructure.postgres.repository.client_repo import ClientRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.client import ClientSchema


router = APIRouter()

