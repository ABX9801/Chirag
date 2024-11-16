from fastapi import FastAPI
from app.api.version1.api_router import router

def create_app():
    app = FastAPI(
        title="Aaradhya"
    )
    app.include_router(router)

    return app

app = create_app()


@app.on_event("startup")
async def startup_event():
    print("Server started")