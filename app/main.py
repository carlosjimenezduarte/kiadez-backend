from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI(title="Kiadez Backend", version="0.1.0")

app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok"}
