from fastapi import FastAPI



def create_app():
    app = FastAPI(
        title="Aaradhya"
    )

    return app

app = create_app()


@app.on_event("startup")
async def startup_event():
    print("Server started")