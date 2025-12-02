from fastapi import FastAPI
from routers import general, llm

def create_app():
    app = FastAPI(title="LLM Backend API")

    # Include routers
    app.include_router(general.router)
    app.include_router(llm.router, prefix="/llm", tags=["LLM"])

    return app

app = create_app()
