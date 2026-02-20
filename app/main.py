from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import router as auth_router
from app.life_purpose.routes import router as life_purpose_router
from app.media.routes import router as media_router
from app.vault.routes import router as vault_router
from app.core.config import settings
from app.support.routes import router as support_router
from app.posts.routes import router as posts_router
from app.biography.routes import router as biography_router
from app.public_wishes.routes import router as public_wishes_router
from app.private_wishes.routes import router as private_wishes_router
from app.oracle.routes import router as oracle_router
from app.follows.routes import router as follows_router
from app.privacy.routes import router as privacy_router
from app.guardian_center.routes import router as guardian_center_router
from app.messages.routes import router as messages_router
from app.achievements.routes import router as achievements_router
from app.gallery.routes import router as gallery_router
from app.calendar.routes import router as calendar_router


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
app.include_router(follows_router)
app.include_router(privacy_router)
app.include_router(guardian_center_router)
app.include_router(messages_router)
app.include_router(achievements_router)
app.include_router(gallery_router)
app.include_router(calendar_router)


@app.get("/health")
def health():
    return {"status": "ok"}
