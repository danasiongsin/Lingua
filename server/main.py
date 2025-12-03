from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import general, llm

def create_app():
    app = FastAPI(title="Lingua Language Learning API")

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5174"],  # React dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(general.router)
    app.include_router(llm.router, prefix="/llm", tags=["LLM"])

    return app

app = create_app()
