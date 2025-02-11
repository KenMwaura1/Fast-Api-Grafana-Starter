from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram
from contextlib import asynccontextmanager

from app.api import ping, notes
from app.db import engine, metadata, database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

metadata.create_all(engine)

app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

# Include your routers
app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes")

