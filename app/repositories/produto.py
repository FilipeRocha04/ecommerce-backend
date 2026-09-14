import uuid
from decimal import Decimal

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.models.compatibilidade import CompatibilidadeProdutoVeiculo
from app.models.produto import Produto


class FiltrosProduto:
    def __init__(
        self,
        *,
        categoria_id: uuid.UUID | None = None,
        marca_id: uuid.UUID | None = None,
        preco_minimo: Decimal | None = None,
        preco_maximo: Decimal | None = None,
        variante_veiculo_id: uuid.UUID | None = None,
        termo_busca: str | None = None,
        apenas_ativos: bool = True,
    ):
        self.categoria_id = categoria_id
        self.marca_id = marca_id
        self.preco_minimo = preco_minimo
        self.preco_maximo = preco_maximo
        self.variante_veiculo_id = variante_veiculo_id
        self.termo_busca = termo_busca
        self.apenas_ativos = apenas_ativos


class ProdutoRepository:
    def __init__(self, db: Session):
        self.db = db

    def _query_base(self, filtros: FiltrosProduto) -> Select:
        query = select(Produto)

        if filtros.apenas_ativos:
            query = query.where(Produto.ativo.is_(True))
        if filtros.categoria_id is not None:
            query = query.where(Produto.categoria_id == filtros.categoria_id)
        if filtros.marca_id is not None:
            query = query.where(Produto.marca_id == filtros.marca_id)
        if filtros.preco_minimo is not None:
            query = query.where(Produto.preco >= filtros.preco_minimo)
        if filtros.preco_maximo is not None:
            query = query.where(Produto.preco <= filtros.preco_maximo)
        if filtros.variante_veiculo_id is not None:
            query = query.where(
                Produto.id.in_(
                    select(CompatibilidadeProdutoVeiculo.produto_id).where(
                        CompatibilidadeProdutoVeiculo.variante_veiculo_id
                        == filtros.variante_veiculo_id
                    )
                )
            )
        if filtros.termo_busca:
            termo = f"%{filtros.termo_busca}%"
            query = query.where(
                or_(
                    Produto.nome.ilike(termo),
                    Produto.descricao.ilike(termo),
                    Produto.codigo_peca.ilike(termo),
                    Produto.sku.ilike(termo),
                )
            )
        return query

    def listar(
        self, filtros: FiltrosProduto, *, offset: int, limite: int
    ) -> tuple[list[Produto], int]:
        query_base = self._query_base(filtros)

        total = self.db.scalar(select(func.count()).select_from(query_base.subquery())) or 0

        query = (
            query_base.options(
                joinedload(Produto.imagens),
                joinedload(Produto.especificacao),
                joinedload(Produto.marca),
                joinedload(Produto.categoria),
            )
            .order_by(Produto.nome)
            .offset(offset)
            .limit(limite)
        )
        itens = self.db.execute(query).unique().scalars().all()
        return list(itens), total

    def obter_por_id(self, produto_id: uuid.UUID) -> Produto | None:
        query = (
            select(Produto)
            .where(Produto.id == produto_id)
            .options(
                joinedload(Produto.imagens),
                joinedload(Produto.especificacao),
                joinedload(Produto.marca),
                joinedload(Produto.categoria),
            )
        )
        return self.db.execute(query).unique().scalar_one_or_none()

    def existe_sku(self, sku: str) -> bool:
        return self.db.scalar(select(Produto.id).where(Produto.sku == sku)) is not None
