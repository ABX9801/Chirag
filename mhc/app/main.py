from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.core.config import settings


def create_app():
    app = FastAPI(
        title="Aaradhya"
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_app()


@app.on_event("startup")
async def startup_event():
    print("Server started")