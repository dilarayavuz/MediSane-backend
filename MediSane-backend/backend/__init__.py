from fastapi import FastAPI
from . import server
from .server import endpoint
from .config import app_config
from backend.callers.db import create_db_engine

backend = FastAPI(
    debug=True,
    title=app_config.app_name,
    description=(
        app_config.app_description
    ),
    version=app_config.app_version,
    docs_url="/docs"
)

for router in server.__all__:
    backend.include_router(**getattr(server, router).__dict__)

engine = create_db_engine()


@backend.get("/")
def index():
    return {
        "app": app_config.app_name,
        "version":  app_config.app_version,
        "description": app_config.app_description
    }
