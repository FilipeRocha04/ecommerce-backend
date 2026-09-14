class ErroDominio(Exception):
    """Erro base de regra de negócio, traduzido para uma resposta HTTP consistente."""

    status_code: int = 400
    codigo: str = "erro_interno"

    def __init__(self, mensagem: str, codigo: str | None = None):
        self.mensagem = mensagem
        if codigo:
            self.codigo = codigo
        super().__init__(mensagem)


class RecursoNaoEncontrado(ErroDominio):
    status_code = 404
    codigo = "recurso_nao_encontrado"

    def __init__(self, mensagem: str = "Recurso não encontrado.", codigo: str | None = None):
        super().__init__(mensagem, codigo)


class ConflitoDados(ErroDominio):
    status_code = 409
    codigo = "conflito_dados"

    def __init__(self, mensagem: str = "Conflito de dados.", codigo: str | None = None):
        super().__init__(mensagem, codigo)


class DadosInvalidos(ErroDominio):
    status_code = 422
    codigo = "dados_invalidos"

    def __init__(self, mensagem: str = "Dados inválidos.", codigo: str | None = None):
        super().__init__(mensagem, codigo)
