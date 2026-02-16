from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import router as auth_router
from app.life_purpose.routes import router as life_purpose_router
from app.media.routes import router as media_router
from app.vault.routes import router as vault_router
from app.core.config import settings
from app.support.routes import router as support_router
from app.dev.routes import router as dev_router
from app.posts.routes import router as posts_router
from app.biography.routes import router as biography_router
from app.public_wishes.routes import router as public_wishes_router
from app.private_wishes.routes import router as private_wishes_router
from app.oracle.routes import router as oracle_router


app = FastAPI(
    title="Kiadez Backend",
    version="0.1.0",
)

def _parse_cors_origins(raw: str) -> list[str]:
    return [origin.strip() for origin in raw.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_cors_origins(settings.CORS_ALLOW_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(life_purpose_router)
app.include_router(media_router)
app.include_router(vault_router)
app.include_router(support_router)
app.include_router(posts_router)
app.include_router(biography_router)
app.include_router(public_wishes_router)
app.include_router(private_wishes_router)
app.include_router(oracle_router)

if settings.APP_ENV.lower() in {"dev", "local", "test"} and settings.DEV_LOGIN_AS_ENABLED:
    app.include_router(dev_router)


@app.get("/health")
def health():
    return {"status": "ok"}
