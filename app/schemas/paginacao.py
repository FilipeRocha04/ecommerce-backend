from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Pagina(BaseModel, Generic[T]):
    itens: list[T]
    pagina: int
    tamanho_pagina: int
    total: int
    total_paginas: int

    @classmethod
    def criar(cls, itens: list[T], total: int, pagina: int, tamanho_pagina: int) -> "Pagina[T]":
        total_paginas = (total + tamanho_pagina - 1) // tamanho_pagina if tamanho_pagina else 0
        return cls(
            itens=itens,
            pagina=pagina,
            tamanho_pagina=tamanho_pagina,
            total=total,
            total_paginas=total_paginas,
        )
