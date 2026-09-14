"""Popula o banco com dados fictícios de desenvolvimento.

Os dados aqui não representam compatibilidade automotiva real; servem apenas
para exercitar o catálogo, a busca e a verificação de compatibilidade.
"""

import random
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.categoria import Categoria
from app.models.compatibilidade import CompatibilidadeProdutoVeiculo
from app.models.estoque import Estoque
from app.models.marca import Marca
from app.models.produto import EspecificacaoProduto, ImagemProduto, Produto
from app.models.veiculo import FabricanteVeiculo, ModeloVeiculo, VarianteVeiculo

FABRICANTES_E_MODELOS = {
    "Volkswagen": ["Gol", "Polo", "T-Cross"],
    "Chevrolet": ["Onix", "Tracker"],
    "Fiat": ["Argo", "Strada"],
    "Toyota": ["Corolla"],
    "Honda": ["Civic"],
}

MARCAS_PECAS = ["Bosch", "TRW", "NGK", "Cofap", "Monroe", "Tecfil"]

CATEGORIAS = {
    "Freios": ["Pastilhas", "Discos", "Fluidos"],
    "Filtros": ["Óleo", "Ar", "Combustível"],
    "Motor": ["Ignição", "Correias", "Arrefecimento"],
    "Suspensão": [],
    "Elétrica": [],
}

PRODUTOS_POR_CATEGORIA = {
    "Pastilhas": [
        {
            "nome": "Pastilha de Freio Dianteira",
            "especificacoes": {"material": "ceramica", "posicao": "dianteira", "sensor": False},
        },
        {
            "nome": "Pastilha de Freio Traseira",
            "especificacoes": {"material": "semi-metalica", "posicao": "traseira", "sensor": True},
        },
        {
            "nome": "Pastilha de Freio Dianteira Esportiva",
            "especificacoes": {"material": "ceramica", "posicao": "dianteira", "sensor": True},
        },
    ],
    "Discos": [
        {
            "nome": "Disco de Freio Ventilado",
            "especificacoes": {"diametro_mm": 260, "ventilado": True},
        },
        {
            "nome": "Disco de Freio Sólido",
            "especificacoes": {"diametro_mm": 236, "ventilado": False},
        },
    ],
    "Fluidos": [
        {
            "nome": "Fluido de Freio DOT 4",
            "especificacoes": {"tipo": "DOT 4", "volume_litros": 0.5},
        },
        {
            "nome": "Fluido de Freio DOT 3",
            "especificacoes": {"tipo": "DOT 3", "volume_litros": 0.5},
        },
    ],
    "Óleo": [
        {"nome": "Filtro de Óleo", "especificacoes": {"rosca": "3/4-16"}},
        {
            "nome": "Óleo Motor 5W30",
            "especificacoes": {
                "viscosidade": "5W30",
                "volume_litros": 1,
                "especificacao": "API SP",
            },
        },
        {
            "nome": "Óleo Motor 10W40",
            "especificacoes": {
                "viscosidade": "10W40",
                "volume_litros": 1,
                "especificacao": "API SN",
            },
        },
    ],
    "Ar": [
        {"nome": "Filtro de Ar do Motor", "especificacoes": {"formato": "painel"}},
        {
            "nome": "Filtro de Ar Condicionado",
            "especificacoes": {"formato": "cabine", "carvao_ativado": True},
        },
    ],
    "Combustível": [
        {"nome": "Filtro de Combustível", "especificacoes": {"pressao_maxima_bar": 5}},
    ],
    "Ignição": [
        {"nome": "Vela de Ignição", "especificacoes": {"eletrodo": "iridio", "rosca_mm": 14}},
        {"nome": "Cabo de Vela", "especificacoes": {"resistencia_ohm": 4000}},
        {"nome": "Bobina de Ignição", "especificacoes": {"tensao_saida_kv": 30}},
    ],
    "Correias": [
        {"nome": "Correia Dentada", "especificacoes": {"dentes": 122}},
        {"nome": "Correia Poly-V", "especificacoes": {"canais": 6}},
    ],
    "Arrefecimento": [
        {"nome": "Bomba d'Água", "especificacoes": {"material": "aluminio"}},
        {"nome": "Radiador", "especificacoes": {"material": "aluminio_plastico"}},
        {"nome": "Válvula Termostática", "especificacoes": {"temperatura_abertura_c": 88}},
    ],
}


def slugify(texto: str) -> str:
    tabela = str.maketrans("áàâãéêíóôõúüç", "aaaaeeiooouuc")
    return texto.lower().translate(tabela).replace(" ", "-").replace("'", "")


def seed(db: Session) -> None:
    fabricantes: dict[str, FabricanteVeiculo] = {}
    variantes: list[VarianteVeiculo] = []

    for nome_fabricante, modelos in FABRICANTES_E_MODELOS.items():
        fabricante = FabricanteVeiculo(nome=nome_fabricante)
        db.add(fabricante)
        db.flush()
        fabricantes[nome_fabricante] = fabricante

        for nome_modelo in modelos:
            modelo = ModeloVeiculo(fabricante_id=fabricante.id, nome=nome_modelo)
            db.add(modelo)
            db.flush()

            for motor, combustivel, cambio, ano_inicio, ano_fim in [
                ("1.0", "Flex", "Manual", 2018, 2021),
                ("1.6", "Flex", "Manual", 2019, 2022),
                ("2.0", "Flex", "Automático", 2020, 2023),
            ]:
                variante = VarianteVeiculo(
                    modelo_id=modelo.id,
                    ano_inicio=ano_inicio,
                    ano_fim=ano_fim,
                    motor=motor,
                    versao=f"{nome_modelo} {motor}",
                    combustivel=combustivel,
                    cambio=cambio,
                )
                db.add(variante)
                variantes.append(variante)
    db.flush()

    marcas: dict[str, Marca] = {}
    for nome_marca in MARCAS_PECAS:
        marca = Marca(nome=nome_marca, slug=slugify(nome_marca))
        db.add(marca)
        marcas[nome_marca] = marca
    db.flush()

    categorias: dict[str, Categoria] = {}
    for nome_categoria, subcategorias in CATEGORIAS.items():
        categoria = Categoria(nome=nome_categoria, slug=slugify(nome_categoria))
        db.add(categoria)
        db.flush()
        categorias[nome_categoria] = categoria

        for nome_sub in subcategorias:
            subcategoria = Categoria(
                categoria_pai_id=categoria.id, nome=nome_sub, slug=slugify(nome_sub)
            )
            db.add(subcategoria)
            db.flush()
            categorias[nome_sub] = subcategoria
    db.flush()

    contador_sku = 1
    produtos: list[Produto] = []
    for nome_subcategoria, especificacoes_produtos in PRODUTOS_POR_CATEGORIA.items():
        categoria = categorias[nome_subcategoria]
        for dados_produto in especificacoes_produtos:
            marca = marcas[random.choice(MARCAS_PECAS)]
            sku = f"SKU-{contador_sku:05d}"
            nome_completo = f"{dados_produto['nome']} {marca.nome}"
            produto = Produto(
                sku=sku,
                marca_id=marca.id,
                categoria_id=categoria.id,
                nome=nome_completo,
                slug=f"{slugify(nome_completo)}-{contador_sku}",
                descricao=f"{dados_produto['nome']} de reposição, marca {marca.nome}.",
                codigo_peca=f"COD-{contador_sku:05d}",
                preco=Decimal(random.randrange(3990, 89990)) / 100,
                meses_garantia=random.choice([3, 6, 12]),
            )
            db.add(produto)
            db.flush()

            db.add(
                ImagemProduto(
                    produto_id=produto.id, url=f"https://picsum.photos/seed/{sku}/400", posicao=0
                )
            )
            db.add(
                EspecificacaoProduto(
                    produto_id=produto.id, especificacoes=dados_produto["especificacoes"]
                )
            )
            db.add(
                Estoque(
                    produto_id=produto.id,
                    quantidade=random.randint(0, 50),
                    quantidade_reservada=0,
                )
            )

            for variante in random.sample(variantes, k=min(4, len(variantes))):
                db.add(
                    CompatibilidadeProdutoVeiculo(
                        produto_id=produto.id, variante_veiculo_id=variante.id
                    )
                )

            produtos.append(produto)
            contador_sku += 1

    db.commit()
    print(
        f"Seed concluído: {len(fabricantes)} fabricantes, {len(variantes)} variantes, "
        f"{len(marcas)} marcas, {len(categorias)} categorias, {len(produtos)} produtos."
    )


def main() -> None:
    with SessionLocal() as db:
        if db.query(Produto).count() > 0:
            print("Banco já possui produtos. Seed não executado para evitar duplicidade.")
            return
        seed(db)


if __name__ == "__main__":
    main()
