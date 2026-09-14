import enum


class StatusCarrinho(str, enum.Enum):
    ATIVO = "ativo"
    CONVERTIDO = "convertido"
    ABANDONADO = "abandonado"


class StatusPedido(str, enum.Enum):
    AGUARDANDO_PAGAMENTO = "aguardando_pagamento"
    PAGAMENTO_APROVADO = "pagamento_aprovado"
    SEPARANDO_PEDIDO = "separando_pedido"
    ENVIADO = "enviado"
    SAIU_PARA_ENTREGA = "saiu_para_entrega"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"


class Canal(str, enum.Enum):
    WEB = "web"
    ASSISTENTE = "assistente"
