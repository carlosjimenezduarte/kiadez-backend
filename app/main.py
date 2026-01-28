from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import router as auth_router
from app.life_purpose.routes import router as life_purpose_router
from app.vault.routes import router as vault_router


app = FastAPI(
    title="Kiadez Backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(life_purpose_router)
app.include_router(vault_router)


@app.get("/health")
def health():
    return {"status": "ok"}
