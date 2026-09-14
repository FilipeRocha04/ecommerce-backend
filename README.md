# Backend — E-commerce Inteligente de Autopeças

API do e-commerce de autopeças. Serve tanto o e-commerce tradicional quanto, futuramente, o
assistente de compras baseado em IA — ambos consultam o mesmo catálogo, estoque, carrinho e
pedidos através desta API, sem regra de negócio duplicada.

## Arquitetura

```text
Route (app/api/routes)
  ↓ HTTP, validação de entrada/saída, status codes
Service (app/services)
  ↓ regras de negócio e validações de domínio
Repository (app/repositories)
  ↓ acesso ao banco via SQLAlchemy
PostgreSQL
```

- **Model** (`app/models`): mapeamento SQLAlchemy 2.x das tabelas.
- **Schema** (`app/schemas`): contratos Pydantic de entrada/saída da API.
- **Repository**: apenas queries e persistência, sem regra de negócio.
- **Service**: validações (produto ativo, estoque, compatibilidade, quantidade) e orquestração
  entre repositories. É aqui que vive a regra "esta peça é compatível com este veículo?".
- **Route**: só lida com HTTP; nunca executa SQL diretamente.

O domínio (tabelas, colunas, rotas, respostas) está em português; nomes de tecnologias e campos
técnicos universais (`id`, `created_at`, `updated_at`) permanecem em inglês.

## Tecnologias

- Python 3.12 / FastAPI / Pydantic
- PostgreSQL + SQLAlchemy 2.x + Alembic
- pytest + Ruff
- Docker / Docker Compose

## Requisitos

- Python 3.12+
- Docker e Docker Compose (para subir o PostgreSQL local)

## Configuração

```bash
cp .env.example .env
```

Variáveis de ambiente (`.env`):

```env
APP_ENV=development
SECRET_KEY=troque-por-um-valor-seguro
DATABASE_URL=postgresql+psycopg://autopecas:autopecas@localhost:5434/autopecas
```

`.env` nunca deve ser versionado (já está no `.gitignore`).

## Subindo com Docker

```bash
docker compose up -d
```

Isso sobe dois serviços:

- `postgres`: PostgreSQL 16 com volume persistente, exposto em `localhost:5434` (host) /
  `postgres:5432` (dentro da rede Docker — é assim que o serviço `backend` acessa o banco).
- `backend`: FastAPI, exposto em `localhost:8000`.

Depois de subir, execute as migrations e o seed (veja abaixo) dentro do container ou apontando
`DATABASE_URL` para `localhost:5434` a partir do host.

## Rodando localmente sem Docker

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -e ".[dev]"

docker compose up -d postgres   # só o banco
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload
```

## Migrations (Alembic)

```bash
alembic upgrade head                          # aplica todas as migrations
alembic revision --autogenerate -m "mensagem" # gera uma nova migration a partir dos models
```

`Base.metadata.create_all()` não é utilizado como substituto de migrations no fluxo normal da
aplicação — apenas os testes usam esse atalho para criar o schema no banco de testes.

## Seed de desenvolvimento

```bash
python -m scripts.seed
```

Popula fabricantes, modelos, variantes de veículos, marcas, categorias (hierárquicas), ~20
produtos fictícios, estoque e compatibilidade produto↔veículo. Os dados são fictícios — **não**
representam compatibilidade automotiva real. O script não roda duas vezes sobre o mesmo banco
(aborta se já houver produtos).

## Testes

```bash
pytest
```

Os testes usam um banco de testes separado (nunca o banco de desenvolvimento/produção), definido
por `DATABASE_URL` no momento em que os testes rodam — configure uma URL apontando para um banco
dedicado (ex.: `autopecas_test`) antes de rodar `pytest`, ou exporte a variável de ambiente
correspondente. O schema desse banco é criado/removido automaticamente pela fixture de sessão em
`app/tests/conftest.py`.

## Lint e formatação

```bash
ruff check .
ruff format .
```

## Swagger / OpenAPI

Com o servidor rodando, acesse:

```text
http://localhost:8000/docs
```

As rotas estão organizadas nas tags Produtos, Categorias, Marcas, Veículos, Compatibilidade,
Estoque, Carrinhos, Pedidos e Saúde.

## Estrutura de pastas

```text
backend/
├── app/
│   ├── main.py              # criação do FastAPI, wiring de rotas e tratamento de erros
│   ├── core/                # configuração, conexão com o banco, exceções de domínio
│   ├── models/               # entidades SQLAlchemy
│   ├── schemas/              # contratos Pydantic
│   ├── repositories/         # acesso ao banco
│   ├── services/              # regras de negócio
│   ├── api/routes/           # endpoints HTTP
│   └── tests/                 # testes pytest
├── alembic/                  # migrations
├── scripts/seed.py           # dados fictícios de desenvolvimento
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Principais rotas

```text
GET    /health
GET    /health/database

GET    /api/v1/categorias
GET    /api/v1/categorias/{categoria_id}

GET    /api/v1/marcas
GET    /api/v1/marcas/{marca_id}

GET    /api/v1/produtos
GET    /api/v1/produtos/buscar?q=...
GET    /api/v1/produtos/{produto_id}
GET    /api/v1/produtos/{produto_id}/estoque

GET    /api/v1/veiculos/fabricantes
GET    /api/v1/veiculos/fabricantes/{fabricante_id}
GET    /api/v1/veiculos/modelos
GET    /api/v1/veiculos/modelos/{modelo_id}
GET    /api/v1/veiculos/variantes
GET    /api/v1/veiculos/variantes/{variante_id}

GET    /api/v1/compatibilidade?produto_id=...&variante_veiculo_id=...

POST   /api/v1/carrinhos
GET    /api/v1/carrinhos/{carrinho_id}
POST   /api/v1/carrinhos/{carrinho_id}/itens
PATCH  /api/v1/carrinhos/{carrinho_id}/itens/{item_id}
DELETE /api/v1/carrinhos/{carrinho_id}/itens/{item_id}

POST   /api/v1/pedidos
GET    /api/v1/pedidos?usuario_id=...
GET    /api/v1/pedidos/{pedido_id}
```

## Sobre o assistente de IA (futuro)

Este backend **não** implementa o agente de IA. As rotas acima foram desenhadas para,
futuramente, serem chamadas como tools por um agente (LangGraph ou similar): o LLM nunca terá
preço, estoque ou compatibilidade hardcoded — tudo é consultado nesta API, a mesma usada pelo
e-commerce tradicional.

## Nota sobre a coexistência com o frontend

O frontend (`../frontend`) já possui uma modelagem própria do mesmo domínio em TypeScript/Drizzle
(`frontend/src/db`). Este backend Python foi implementado como um serviço independente, com banco
de dados próprio, conforme decisão explícita ao iniciar este projeto — os dois não compartilham
banco nem schema neste momento.
