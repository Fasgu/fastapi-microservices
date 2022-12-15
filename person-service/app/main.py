import logging

from fastapi import FastAPI

from app.api import persons
from app.db import init_db


def create_application() -> FastAPI:
    application = FastAPI(
        openapi_url="/persons/openapi.json",
        docs_url="/persons/docs")
    application.include_router(
        persons.router,
        tags=["persons"])
    return application


app = create_application()
log = logging.getLogger("uvicorn")


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
