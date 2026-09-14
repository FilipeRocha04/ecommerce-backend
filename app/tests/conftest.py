import os
import uuid
from collections.abc import Generator
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://autopecas:autopecas@localhost:5434/autopecas_test",
)
os.environ["APP_ENV"] = "test"

from app.core.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models.categoria import Categoria  # noqa: E402
from app.models.estoque import Estoque  # noqa: E402
from app.models.marca import Marca  # noqa: E402
from app.models.produto import Produto  # noqa: E402
from app.models.usuario import Usuario  # noqa: E402
from app.models.veiculo import FabricanteVeiculo, ModeloVeiculo, VarianteVeiculo  # noqa: E402

TEST_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def preparar_banco() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    session = TestSessionLocal()
    yield session
    session.close()


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    def _get_db_override() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def marca(db: Session) -> Marca:
    marca = Marca(nome=f"Marca {uuid.uuid4().hex[:8]}", slug=f"marca-{uuid.uuid4().hex[:8]}")
    db.add(marca)
    db.flush()
    return marca


@pytest.fixture
def categoria(db: Session) -> Categoria:
    categoria = Categoria(
        nome=f"Categoria {uuid.uuid4().hex[:8]}", slug=f"categoria-{uuid.uuid4().hex[:8]}"
    )
    db.add(categoria)
    db.flush()
    return categoria


@pytest.fixture
def fabricante(db: Session) -> FabricanteVeiculo:
    fabricante = FabricanteVeiculo(nome=f"Fabricante {uuid.uuid4().hex[:8]}")
    db.add(fabricante)
    db.flush()
    return fabricante


@pytest.fixture
def modelo(db: Session, fabricante: FabricanteVeiculo) -> ModeloVeiculo:
    modelo = ModeloVeiculo(fabricante_id=fabricante.id, nome=f"Modelo {uuid.uuid4().hex[:8]}")
    db.add(modelo)
    db.flush()
    return modelo


@pytest.fixture
def variante(db: Session, modelo: ModeloVeiculo) -> VarianteVeiculo:
    variante = VarianteVeiculo(
        modelo_id=modelo.id,
        ano_inicio=2019,
        ano_fim=2022,
        motor="1.6",
        versao="1.6 MSI",
        combustivel="Flex",
        cambio="Manual",
    )
    db.add(variante)
    db.flush()
    return variante


@pytest.fixture
def usuario(db: Session) -> Usuario:
    usuario = Usuario(
        nome="Usuário Teste",
        email=f"usuario-{uuid.uuid4().hex[:8]}@teste.com",
        senha_hash="hash-fake",
    )
    db.add(usuario)
    db.flush()
    return usuario


@pytest.fixture
def produto(db: Session, marca: Marca, categoria: Categoria) -> Produto:
    produto = Produto(
        sku=f"SKU-{uuid.uuid4().hex[:10]}",
        marca_id=marca.id,
        categoria_id=categoria.id,
        nome="Pastilha de Freio Teste",
        slug=f"produto-{uuid.uuid4().hex[:8]}",
        descricao="Produto de teste.",
        codigo_peca="COD-TESTE",
        preco=Decimal("199.90"),
    )
    db.add(produto)
    db.flush()
    db.add(Estoque(produto_id=produto.id, quantidade=10, quantidade_reservada=2))
    db.flush()
    return produto
