from fastapi import FastAPI
from app.api.version1.api_router import router
from starlette.middleware.cors import CORSMiddleware

def create_app():
    app = FastAPI(
        title="Aaradhya"
    )
    app.include_router(router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()


@app.on_event("startup")
async def startup_event():
    print("Server started")