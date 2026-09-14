# Backend — E-commerce Inteligente de Autopeças

Quero que você analise este projeto e implemente a primeira versão do backend do meu **E-commerce Inteligente de Autopeças**.

## Importante

Antes de criar, remover ou alterar qualquer arquivo, analise completamente a estrutura atual do projeto.

Identifique:

- tecnologias utilizadas;
- estrutura de diretórios;
- frontend existente;
- backend existente, caso exista;
- package managers;
- configurações;
- Docker/Docker Compose existentes;
- variáveis de ambiente;
- banco existente;
- models existentes;
- migrations existentes;
- padrões arquiteturais já utilizados;
- autenticação existente, caso exista.

Não crie uma arquitetura paralela desnecessária.

Se o projeto já possuir uma estrutura adequada, adapte a implementação a ela.

Antes de implementar qualquer coisa:

1. Analise o projeto.
2. Explique resumidamente o que já existe.
3. Apresente o plano de implementação.
4. Liste os principais arquivos que pretende criar ou modificar.
5. Identifique possíveis conflitos com a arquitetura existente.
6. Depois disso, implemente.

---

# 1. Contexto do projeto

O projeto é um e-commerce especializado em peças automotivas.

Existirão dois canais principais de compra:

1. E-commerce tradicional.
2. Assistente de compras baseado em IA.

No e-commerce tradicional, o cliente poderá:

- navegar pelo catálogo;
- pesquisar produtos;
- selecionar seu veículo;
- verificar compatibilidade;
- adicionar produtos ao carrinho;
- realizar checkout;
- criar pedidos.

No futuro, haverá também um assistente conversacional semelhante a aplicativos de mensagens.

### Exemplo

Cliente:

> Preciso de pastilhas de freio para um Gol 1.6 2020.

O assistente deverá:

1. identificar o veículo;
2. consultar produtos;
3. verificar compatibilidade;
4. consultar estoque;
5. recomendar produtos.

Depois:

Cliente:

> Adiciona a Bosch no carrinho.

O agente utilizará uma tool/API do backend para adicionar o produto.

## Regra importante

O e-commerce tradicional e o assistente utilizarão o **mesmo**:

- catálogo;
- banco;
- estoque;
- clientes;
- veículos;
- carrinho;
- pedidos.

O agente de IA não terá preços, produtos, estoque ou compatibilidade hardcoded no prompt.

Essas informações serão sempre consultadas no backend.

---

# 2. Objetivo desta implementação

Nesta primeira etapa quero construir uma fundação sólida do backend.

O foco será:

- banco de dados;
- models;
- migrations;
- repositories;
- services;
- schemas;
- APIs;
- produtos;
- categorias;
- marcas;
- veículos;
- compatibilidade;
- estoque;
- estrutura inicial de usuários;
- estrutura inicial de carrinho;
- estrutura inicial de pedidos;
- tracking básico;
- testes;
- Docker.

## Não implementar ainda

Ainda **não** quero implementar:

- agente de IA;
- LangGraph;
- embeddings;
- banco vetorial;
- Elasticsearch;
- Kafka;
- Redpanda;
- MinIO;
- Data Lake;
- Parquet;
- DuckDB;
- dbt;
- Airflow;
- Dagster;
- Machine Learning;
- MLflow;
- Kubernetes;
- microserviços.

Não adicione essas tecnologias agora.

A arquitetura inicial deve permanecer simples.

---

# 3. Stack

## Backend

- Python
- FastAPI
- Pydantic

## Banco

- PostgreSQL

## ORM

- SQLAlchemy 2.x

## Migrations

- Alembic

## Qualidade

- pytest
- Ruff

## Infraestrutura local

- Docker
- Docker Compose

Utilize versões estáveis e atuais compatíveis entre si.

Não introduza bibliotecas desnecessárias.

---

# 4. Idioma e padrão de nomenclatura

O domínio da aplicação deverá estar em **português**.

Quero português para:

- tabelas;
- colunas relacionadas ao domínio;
- entidades;
- models;
- schemas;
- repositories;
- services;
- funções relacionadas ao domínio;
- rotas;
- parâmetros;
- respostas das APIs;
- enums do negócio.

### Não utilizar

```text
products
categories
vehicles
vehicle_models
cart_items
orders
```

### Utilizar

```text
produtos
categorias
veiculos
modelos_veiculos
itens_carrinho
pedidos
```

As rotas também deverão estar em português.

Exemplo:

```text
/api/v1/produtos
/api/v1/categorias
/api/v1/marcas
/api/v1/veiculos
/api/v1/compatibilidade
/api/v1/carrinhos
/api/v1/pedidos
```

Não traduza nomes próprios de tecnologias.

Continuar utilizando normalmente:

```text
FastAPI
PostgreSQL
SQLAlchemy
Alembic
Docker
Docker Compose
JSONB
UUID
HTTP
API
```

Para campos técnicos universais como:

```text
id
created_at
updated_at
```

pode manter esses nomes em inglês para seguir convenções comuns.

O mais importante é não misturar o domínio em português e inglês sem necessidade.

---

# 5. Arquitetura do backend

Quero uma aplicação modular.

Uma estrutura possível:

```text
backend/
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── exceptions.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   │
│   ├── api/
│   │   └── routes/
│   │
│   └── tests/
│
├── alembic/
├── alembic.ini
├── Dockerfile
├── pyproject.toml
└── .env.example
```

Porém, **não siga essa estrutura cegamente**.

Primeiro analise o projeto existente.

Se já houver uma organização adequada, preserve-a.

Quero uma separação conceitual semelhante a:

```text
Route
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

## Route

Responsável por:

- HTTP;
- parâmetros;
- status codes;
- request;
- response;
- dependências.

## Service

Responsável por:

- regras de negócio;
- validações de domínio;
- operações envolvendo múltiplos repositories.

## Repository

Responsável por:

- acesso ao banco;
- queries;
- persistência.

## Model

Responsável pelo mapeamento SQLAlchemy.

## Schema

Responsável pelos contratos Pydantic da API.

Não coloque regras de negócio importantes diretamente nas routes.

Também não crie abstrações exageradas apenas para seguir padrões.

---

# 6. Configuração

Utilizar variáveis de ambiente.

Exemplos:

```env
DATABASE_URL=
APP_ENV=
SECRET_KEY=
```

Criar:

```text
.env.example
```

Nunca colocar credenciais reais no código.

Nunca versionar:

```text
.env
```

Certifique-se de que `.env` esteja no `.gitignore`.

---

# 7. PostgreSQL

O PostgreSQL será a fonte de verdade transacional da aplicação.

Preferencialmente utilizar UUID como identificador das entidades principais.

Utilizar `TIMESTAMPTZ` para timestamps importantes.

Utilizar:

```text
created_at
updated_at
```

onde fizer sentido.

## Valores monetários

Nunca utilizar `float`.

Utilizar:

- `NUMERIC` no PostgreSQL;
- `Decimal` no Python.

Criar adequadamente:

- primary keys;
- foreign keys;
- unique constraints;
- indexes;
- check constraints quando necessário.

Evite índices desnecessários.

---

# 8. Usuários

Criar tabela:

```text
usuarios
```

Campos:

```text
id
nome
email
telefone
senha_hash
created_at
updated_at
```

Regras:

- `email` deve possuir `UNIQUE`.

Não implementar autenticação completa nesta etapa caso ainda não exista no projeto.

A estrutura deve apenas estar preparada para isso.

---

# 9. Endereços

Criar tabela:

```text
enderecos
```

Campos:

```text
id
usuario_id
nome
cep
logradouro
numero
complemento nullable
bairro
cidade
estado
principal
created_at
updated_at
```

Relacionamento:

```text
usuarios 1:N enderecos
```

---

# 10. Veículos

Essa é uma parte crítica do projeto.

Não representar um veículo simplesmente como:

```text
Gol 2020
```

Precisamos representar corretamente:

- fabricante;
- modelo;
- ano;
- motorização;
- versão;
- combustível;
- câmbio.

---

# 11. Fabricantes de veículos

Tabela:

```text
fabricantes_veiculos
```

Campos:

```text
id
nome
created_at
```

Exemplos:

```text
Volkswagen
Chevrolet
Fiat
Toyota
Honda
```

---

# 12. Modelos de veículos

Tabela:

```text
modelos_veiculos
```

Campos:

```text
id
fabricante_id
nome
created_at
```

Relacionamento:

```text
fabricantes_veiculos 1:N modelos_veiculos
```

Exemplo:

```text
Volkswagen
├── Gol
├── Polo
└── T-Cross
```

---

# 13. Variantes de veículos

Tabela:

```text
variantes_veiculos
```

Campos:

```text
id
modelo_id
ano_inicio
ano_fim
motor
versao
combustivel
cambio
created_at
updated_at
```

Exemplo:

```text
Volkswagen
└── Gol
    └── 1.6 MSI
        ├── Flex
        ├── Manual
        └── 2019-2022
```

Essa tabela representa uma configuração específica do veículo.

---

# 14. Garagem do usuário

Tabela:

```text
veiculos_usuarios
```

Campos:

```text
id
usuario_id
variante_veiculo_id
ano
apelido
placa nullable
principal
created_at
updated_at
```

Relacionamentos:

```text
usuarios 1:N veiculos_usuarios

variantes_veiculos 1:N veiculos_usuarios
```

Um usuário poderá possuir vários veículos.

Exemplo:

```text
Usuário
├── Gol 1.6 2020
└── Civic 2.0 2018
```

---

# 15. Marcas de peças

Tabela:

```text
marcas
```

Campos:

```text
id
nome
slug
created_at
```

Exemplos:

```text
Bosch
TRW
NGK
Cofap
Monroe
Tecfil
```

---

# 16. Categorias

Tabela:

```text
categorias
```

Campos:

```text
id
categoria_pai_id nullable
nome
slug
created_at
updated_at
```

As categorias deverão ser hierárquicas.

Exemplo:

```text
Freios
├── Pastilhas
├── Discos
└── Fluidos

Motor
├── Ignição
├── Correias
└── Arrefecimento

Filtros
├── Óleo
├── Ar
└── Combustível
```

Utilizar relacionamento da categoria com ela mesma através de:

```text
categoria_pai_id
```

---

# 17. Produtos

Tabela:

```text
produtos
```

Campos:

```text
id
sku
marca_id
categoria_id
nome
slug
descricao
codigo_peca
preco
preco_promocional nullable
meses_garantia
ativo
created_at
updated_at
```

Regras:

```text
sku UNIQUE
slug UNIQUE
```

Valores monetários utilizando `NUMERIC/Decimal`.

---

# 18. Imagens dos produtos

Tabela:

```text
imagens_produtos
```

Campos:

```text
id
produto_id
url
posicao
created_at
```

Não armazenar imagens binárias diretamente no PostgreSQL.

Armazenar somente referência/URL.

O storage real poderá ser definido futuramente.

---

# 19. Especificações dos produtos

Tabela:

```text
especificacoes_produtos
```

Campos:

```text
id
produto_id
especificacoes JSONB
created_at
updated_at
```

Essa estrutura servirá para atributos que variam muito entre categorias.

### Exemplo para bateria

```json
{
  "voltagem": "12V",
  "capacidade_ah": 60,
  "cca": 450
}
```

### Exemplo para óleo

```json
{
  "viscosidade": "5W30",
  "volume_litros": 1,
  "especificacao": "API SP"
}
```

### Exemplo para pastilha

```json
{
  "material": "ceramica",
  "posicao": "dianteira",
  "sensor": false
}
```

Não criar dezenas de colunas nullable em `produtos` para especificações específicas de determinadas categorias.

---

# 20. Compatibilidade entre produto e veículo

Essa é uma das partes **mais importantes da aplicação**.

Tabela:

```text
compatibilidade_produtos_veiculos
```

Campos:

```text
id
produto_id
variante_veiculo_id
observacoes nullable
created_at
```

Relacionamento:

```text
produtos N:N variantes_veiculos
```

Criar constraint:

```text
UNIQUE(produto_id, variante_veiculo_id)
```

Essa tabela deverá permitir responder de forma determinística:

> Esta peça é compatível com este veículo?

Exemplo:

```text
Pastilha Bosch ABC
│
├── Gol 1.6 MSI 2019-2022
└── Voyage 1.6 2019-2022
```

Não utilizar LLM para decidir compatibilidade.

A compatibilidade deve vir dos dados estruturados da aplicação.

---

# 21. Estoque

Criar:

```text
estoques
```

Campos:

```text
id
produto_id
quantidade
quantidade_reservada
updated_at
```

Não colocar quantidade diretamente na tabela `produtos`.

Isso permitirá futuramente evoluir para estoque por depósito sem alterar completamente o catálogo.

Adicionar validações adequadas para impedir quantidades negativas quando aplicável.

---

# 22. Carrinho

Criar:

```text
carrinhos
```

Campos:

```text
id
usuario_id nullable
sessao_id nullable
status
canal
created_at
updated_at
```

O carrinho poderá pertencer:

- a um usuário autenticado;
- ou temporariamente a uma sessão.

O mesmo carrinho deverá ser utilizado pelo site e futuramente pelo assistente.

Não criar:

```text
carrinho_site
carrinho_assistente
```

Deve existir apenas o domínio de carrinho.

---

# 23. Itens do carrinho

Criar:

```text
itens_carrinho
```

Campos:

```text
id
carrinho_id
produto_id
quantidade
preco_unitario
created_at
updated_at
```

Criar constraint apropriada para evitar duplicação desnecessária do mesmo produto no mesmo carrinho.

Se o produto já estiver no carrinho, a camada de service deverá futuramente conseguir incrementar a quantidade.

---

# 24. Pedidos

Criar:

```text
pedidos
```

Campos:

```text
id
numero_pedido
usuario_id
status
subtotal
desconto
frete
total
canal
endereco_entrega JSONB
created_at
updated_at
```

O endereço de entrega deverá ser armazenado como snapshot.

Não depender apenas da tabela `enderecos`.

Isso é importante porque o usuário poderá alterar o endereço posteriormente, mas o pedido histórico deverá manter o endereço utilizado no momento da compra.

---

# 25. Itens do pedido

Criar:

```text
itens_pedido
```

Campos:

```text
id
pedido_id
produto_id
sku
nome_produto
quantidade
preco_unitario
total
```

Armazenar snapshot de informações importantes do produto.

Exemplo:

```text
Hoje:

Pastilha Bosch = R$ 189,90

Futuramente:

Pastilha Bosch = R$ 229,90

Pedido antigo:

Pastilha Bosch = R$ 189,90
```

---

# 26. Sessões

Criar:

```text
sessoes
```

Campos:

```text
id
usuario_id nullable
iniciada_em
finalizada_em nullable
canal_inicial
```

Essa entidade será utilizada futuramente para reconstrução da jornada do usuário.

---

# 27. Eventos

Criar:

```text
eventos
```

Campos:

```text
id
nome_evento
timestamp
sessao_id nullable
usuario_id nullable
canal
propriedades JSONB
```

Exemplos de eventos futuros:

```text
session_started
vehicle_selected
product_searched
product_viewed
product_recommended
product_added_to_cart
product_removed_from_cart
checkout_started
purchase_completed
purchase_cancelled
```

Mesmo que o nome dos eventos permaneça inicialmente padronizado em inglês para facilitar analytics futuro, documente essa decisão.

As propriedades deverão permitir dados flexíveis.

Exemplo:

```json
{
  "produto_id": "...",
  "quantidade": 1,
  "preco": 189.90
}
```

Nesta etapa os eventos serão persistidos diretamente no PostgreSQL.

**Não adicionar Kafka/Redpanda.**

---

# 28. Enums

Quando fizer sentido, utilize enums para estados controlados.

## Status do carrinho

```text
ativo
convertido
abandonado
```

## Status do pedido

```text
aguardando_pagamento
pagamento_aprovado
separando_pedido
enviado
saiu_para_entrega
entregue
cancelado
```

## Canal

```text
web
assistente
```

Evite strings arbitrárias para estados importantes do domínio.

---

# 29. Rotas

Utilizar prefixo:

```text
/api/v1
```

As rotas relacionadas ao domínio deverão estar em português.

---

# 30. Health Check

Criar:

```http
GET /health
```

Resposta simples indicando que a aplicação está funcionando.

Também criar, se fizer sentido:

```http
GET /health/database
```

para verificar conectividade com PostgreSQL.

---

# 31. Categorias

Criar inicialmente:

```http
GET /api/v1/categorias
GET /api/v1/categorias/{categoria_id}
```

A listagem deverá permitir consultar a hierarquia quando necessário.

---

# 32. Marcas

Criar:

```http
GET /api/v1/marcas
GET /api/v1/marcas/{marca_id}
```

---

# 33. Produtos

Criar:

```http
GET /api/v1/produtos
GET /api/v1/produtos/{produto_id}
GET /api/v1/produtos/buscar?q=pastilha
```

A listagem deverá possuir paginação.

Preparar filtros por:

```text
categoria
marca
preco_minimo
preco_maximo
veiculo
```

Não implementar busca vetorial.

A busca inicial deverá utilizar PostgreSQL.

---

# 34. Veículos

Organizar as rotas preferencialmente assim:

```http
GET /api/v1/veiculos/fabricantes
GET /api/v1/veiculos/fabricantes/{fabricante_id}

GET /api/v1/veiculos/modelos
GET /api/v1/veiculos/modelos/{modelo_id}

GET /api/v1/veiculos/variantes
GET /api/v1/veiculos/variantes/{variante_id}
```

Permitir filtros nas variantes.

Exemplo:

```http
GET /api/v1/veiculos/variantes?fabricante=volkswagen&modelo=gol&ano=2020&motor=1.6
```

---

# 35. Compatibilidade

Criar uma API específica para verificar compatibilidade.

Exemplo:

```http
GET /api/v1/compatibilidade?produto_id=...&variante_veiculo_id=...
```

Resposta esperada:

```json
{
  "compativel": true,
  "produto_id": "...",
  "variante_veiculo_id": "..."
}
```

A regra de compatibilidade deve estar na camada de `service`.

A `route` não deve executar query SQL diretamente.

---

# 36. Estoque

Criar:

```http
GET /api/v1/produtos/{produto_id}/estoque
```

Exemplo de resposta:

```json
{
  "produto_id": "...",
  "quantidade": 8,
  "quantidade_reservada": 1,
  "quantidade_disponivel": 7
}
```

A quantidade disponível deverá ser calculada corretamente.

---

# 37. Carrinhos

Preparar a estrutura para:

```http
POST   /api/v1/carrinhos
GET    /api/v1/carrinhos/{carrinho_id}
POST   /api/v1/carrinhos/{carrinho_id}/itens
PATCH  /api/v1/carrinhos/{carrinho_id}/itens/{item_id}
DELETE /api/v1/carrinhos/{carrinho_id}/itens/{item_id}
```

As regras de carrinho deverão ficar na camada de `service`.

Não permitir:

```text
quantidade <= 0
```

Ao adicionar produto, validar:

- existência;
- produto ativo;
- estoque;
- preço atual.

---

# 38. Pedidos

Preparar estrutura para:

```http
POST /api/v1/pedidos
GET  /api/v1/pedidos
GET  /api/v1/pedidos/{pedido_id}
```

A criação do pedido deverá futuramente utilizar os itens do carrinho.

Não implementar gateway de pagamento real nesta etapa.

---

# 39. Paginação

Criar uma estratégia consistente de paginação.

Exemplo:

```http
?page=1&page_size=20
```

Resposta conceitual:

```json
{
  "itens": [],
  "pagina": 1,
  "tamanho_pagina": 20,
  "total": 150,
  "total_paginas": 8
}
```

Evitar retornar milhares de registros de uma vez.

---

# 40. Erros

Criar tratamento consistente de erros.

Utilizar corretamente:

```text
200
201
204
400
404
409
422
500
```

Exemplos:

```text
Produto não encontrado → 404

Categoria não encontrada → 404

SKU duplicado → 409

Quantidade inválida → 422 ou 400 conforme a situação
```

Não retornar:

- stack trace;
- SQL;
- senha;
- connection string;
- detalhes internos.

Criar respostas de erro consistentes.

Exemplo:

```json
{
  "erro": "produto_nao_encontrado",
  "mensagem": "Produto não encontrado."
}
```

---

# 41. Alembic

Configure Alembic corretamente.

Criar a migration inicial contendo o schema necessário.

Quero conseguir executar:

```bash
alembic upgrade head
```

e criar toda a estrutura do banco.

Não utilizar:

```python
Base.metadata.create_all()
```

como substituto de migrations no ambiente normal da aplicação.

---

# 42. Seed

Criar uma estratégia clara para seed de desenvolvimento.

Adicionar dados fictícios suficientes para testar o sistema.

## Fabricantes

```text
Volkswagen
Chevrolet
Fiat
Toyota
Honda
```

## Modelos

### Volkswagen

```text
Gol
Polo
T-Cross
```

### Chevrolet

```text
Onix
Tracker
```

### Fiat

```text
Argo
Strada
```

### Toyota

```text
Corolla
```

### Honda

```text
Civic
```

Criar algumas variantes.

Exemplo:

```text
Volkswagen Gol
1.6
Flex
Manual
2019-2022
```

## Marcas de peças

```text
Bosch
TRW
NGK
Cofap
Monroe
Tecfil
```

## Categorias

```text
Freios
Filtros
Motor
Suspensão
Elétrica
```

Criar subcategorias relevantes.

Criar aproximadamente **20 produtos fictícios**.

Criar estoque para esses produtos.

Criar relações de compatibilidade.

Quero conseguir testar o cenário:

```text
Veículo
   ↓
Volkswagen Gol
1.6
2020

Pesquisa
   ↓
"pastilha"

Resultado
   ↓
múltiplos produtos

Compatibilidade
   ↓
identificar quais servem no veículo
```

Os dados são fictícios e devem ser claramente tratados como seed de desenvolvimento, não como fonte real de compatibilidade automotiva.

---

# 43. Docker

Docker deve fazer parte da estrutura desde o início.

Criar:

```text
Dockerfile
```

para o backend.

Criar ou adaptar:

```text
docker-compose.yml
```

para desenvolvimento.

Inicialmente quero pelo menos:

```text
Docker Compose
├── backend
│   └── FastAPI
│
└── postgres
    └── PostgreSQL
```

O PostgreSQL deverá utilizar volume persistente.

Configurar:

- network;
- environment variables;
- healthcheck do PostgreSQL;
- dependências adequadas.

O backend deverá conseguir acessar o banco utilizando o nome do serviço Docker, não `localhost` dentro do container.

Não colocar credenciais reais diretamente no `docker-compose`.

---

# 44. Testes

Utilizar `pytest`.

Os testes não devem utilizar banco de produção.

Criar uma estratégia apropriada para banco de testes.

Criar testes iniciais para:

```http
GET /health

GET /api/v1/produtos
GET /api/v1/produtos/{id}
GET /api/v1/produtos/buscar

GET /api/v1/categorias
GET /api/v1/marcas

GET /api/v1/veiculos/fabricantes
GET /api/v1/veiculos/modelos
GET /api/v1/veiculos/variantes

GET /api/v1/compatibilidade

GET /api/v1/produtos/{id}/estoque
```

Testar também casos negativos:

- produto inexistente;
- veículo inexistente;
- compatibilidade inexistente;
- parâmetros inválidos.

---

# 45. Ruff

Configure Ruff.

Quero conseguir executar lint e formatação de maneira consistente.

Não deixar:

- imports não utilizados;
- código morto desnecessário;
- problemas simples de formatação.

---

# 46. OpenAPI / Swagger

Documentar adequadamente as APIs utilizando FastAPI/Pydantic.

Swagger deverá apresentar:

- descrição das rotas;
- parâmetros;
- schemas;
- possíveis respostas;
- exemplos quando fizer sentido.

Quero conseguir abrir:

```text
/docs
```

e entender facilmente a API.

Organize as rotas com tags como:

```text
Produtos
Categorias
Marcas
Veículos
Compatibilidade
Estoque
Carrinhos
Pedidos
```

---

# 47. Performance

Não faça otimizações prematuras.

Porém, evite problemas óbvios.

Analise:

- N+1 queries;
- índices necessários;
- paginação;
- relacionamentos;
- eager/lazy loading quando aplicável.

A compatibilidade entre produto e veículo deverá possuir índices apropriados.

---

# 48. Segurança

Mesmo sendo uma primeira versão:

- não hardcode credenciais;
- não exponha stack traces;
- valide inputs;
- utilize schemas Pydantic;
- não construa SQL manual inseguro;
- não confie em preços enviados pelo frontend;
- não confie em totais enviados pelo frontend.

Preço, estoque e total deverão ser determinados pelo backend.

---

# 49. README

Atualize o README do backend explicando:

1. arquitetura;
2. tecnologias;
3. requisitos;
4. configuração;
5. variáveis de ambiente;
6. Docker;
7. como subir PostgreSQL;
8. como subir FastAPI;
9. como executar migrations;
10. como executar seed;
11. como executar testes;
12. como executar Ruff;
13. como acessar Swagger;
14. estrutura das principais pastas.

Adicionar exemplos de comandos.

---

# 50. Critérios de conclusão

Ao finalizar essa etapa quero conseguir:

1. Clonar o projeto.
2. Criar/configurar `.env`.
3. Executar:

```bash
docker compose up -d
```

4. Ter PostgreSQL funcionando.
5. Ter FastAPI funcionando.
6. Executar:

```bash
alembic upgrade head
```

7. Executar o seed.
8. Abrir `/docs`.
9. Listar produtos.
10. Pesquisar `pastilha`.
11. Encontrar `Gol 1.6 2020`.
12. Verificar se determinado produto é compatível.
13. Consultar estoque.
14. Executar testes.
15. Executar Ruff.

---

# 51. Importante sobre o agente de IA

Não implemente o agente nesta etapa.

Porém, projete as APIs de maneira que futuramente possam ser utilizadas como tools.

Exemplos conceituais futuros:

```python
buscar_produtos()
obter_produto()
verificar_compatibilidade()
consultar_estoque()

obter_carrinho()
adicionar_ao_carrinho()
remover_do_carrinho()

criar_pedido()
obter_pedido()
```

A arquitetura futura será:

```text
Cliente
   ↓
Agente
   ↓
Tool Calling
   ↓
API FastAPI
   ↓
PostgreSQL
```

O LLM será responsável principalmente por:

- entender linguagem natural;
- identificar intenção;
- conduzir a conversa;
- decidir qual tool utilizar.

O backend será responsável por:

- produtos;
- preços;
- estoque;
- compatibilidade;
- carrinho;
- pedidos;
- regras de negócio.

Portanto, nunca coloque preço, estoque ou compatibilidade diretamente no prompt do agente.

---

# 52. Princípio arquitetural

Não quero complexidade apenas para utilizar tecnologias modernas.

Cada tecnologia deverá entrar quando existir um problema concreto que justifique sua utilização.

Neste momento:

```text
FastAPI
   +
PostgreSQL
   +
SQLAlchemy
   +
Alembic
   +
Docker
```

são suficientes.

No futuro poderemos introduzir:

```text
Redis
Redpanda/Kafka
MinIO/S3
Parquet
DuckDB
dbt
Airflow/Dagster
OpenTelemetry
Prometheus
Grafana
MLflow
Kubernetes
```

Mas **não agora**.

---

# 53. Entrega final

Depois de implementar:

1. Mostre a estrutura final de diretórios.
2. Explique resumidamente a arquitetura criada.
3. Liste todas as tabelas criadas.
4. Liste todas as rotas implementadas.
5. Mostre os relacionamentos principais.
6. Informe as migrations criadas.
7. Informe como executar o seed.
8. Informe como subir o ambiente com Docker.
9. Informe como executar os testes.
10. Informe como executar Ruff.
11. Execute os testes disponíveis.
12. Execute o lint.
13. Corrija os problemas encontrados quando forem consequência da implementação.
14. Informe claramente qualquer problema que não tenha conseguido resolver.
15. Não declare que algo está funcionando sem ter verificado quando houver meios para verificar.

Priorize código:

- simples;
- legível;
- testável;
- consistente;
- fácil de evoluir.

O objetivo desta etapa **não é construir toda a plataforma**.

O objetivo é construir uma base sólida para posteriormente evoluir:

```text
E-commerce
    ↓
Assistente de IA
    ↓
Tracking
    ↓
Engenharia de Dados
    ↓
Analytics
    ↓
Machine Learning
    ↓
MLOps
```