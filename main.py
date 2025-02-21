from fastapi import FastAPI

from app.controllers import starwars
from config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

app.include_router(starwars.router)

