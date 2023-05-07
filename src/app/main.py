from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

from app.api import notes, ping
from app.db import engine, metadata, database

metadata.create_all(engine)

app = FastAPI()
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

# Define a counter metric
REQUESTS_COUNT = Counter(
    "requests_total", "Total number of requests", ["method", "endpoint", "status_code"]
)
# Define a histogram metric
REQUESTS_TIME = Histogram("requests_time", "Request processing time", ["method", "endpoint"])
api_request_summary = Histogram("api_request_summary", "Request processing time", ["method", "endpoint"])
api_request_counter = Counter("api_request_counter", "Request processing time", ["method", "endpoint", "http_status"])



@app.get("/notes")
async def get_notes():
    api_request_counter.labels(method="GET", endpoint="/notes", http_status=200).inc()
    api_request_summary.labels(method="GET", endpoint="/notes").observe(0.1)
    return await notes.get_notes()


@app.get("/notes/{id}")
async def get_note_by_id(id: int):
    api_request_counter.labels(method="GET", endpoint="/notes/{id}", http_status=200).inc()
    api_request_summary.labels(method="GET", endpoint="/notes/{id}").observe(0.1)
    return await notes.get_note_by_id(id)



@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(ping.router, tags=["ping"],  responses={404: {"description": "Not found"}})
app.include_router(notes.router, prefix="/notes", tags=["notes"],  responses={404: {"description": "Not found"}})

