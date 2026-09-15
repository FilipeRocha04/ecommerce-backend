from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import (
    assistente,
    carrinhos,
    categorias,
    compatibilidade,
    health,
    marcas,
    pedidos,
    produtos,
    veiculos,
)
from app.core.config import get_settings
from app.core.exceptions import ErroDominio

settings = get_settings()

app = FastAPI(
    title="E-commerce Inteligente de Autopeças",
    description=(
        "API do e-commerce de autopeças, utilizada tanto pelo site tradicional quanto, "
        "futuramente, pelo assistente de compras baseado em IA."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ErroDominio)
def tratar_erro_dominio(request: Request, exc: ErroDominio) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"erro": exc.codigo, "mensagem": exc.mensagem},
    )


app.include_router(health.router)
app.include_router(categorias.router)
app.include_router(marcas.router)
app.include_router(produtos.router)
app.include_router(veiculos.router)
app.include_router(compatibilidade.router)
app.include_router(carrinhos.router)
app.include_router(pedidos.router)
app.include_router(assistente.router)
