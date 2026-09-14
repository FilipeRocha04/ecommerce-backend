from fastapi import APIRouter
from sqlalchemy import text

from app.api.deps import DbSession

router = APIRouter(tags=["Saúde"])


@router.get("/health")
def verificar_saude() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/database")
def verificar_saude_banco(db: DbSession) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
