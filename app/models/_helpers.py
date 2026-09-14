import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

MONEY_PRECISION = 10
MONEY_SCALE = 2


def id_coluna():
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def criado_em_coluna():
    return mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


def atualizado_em_coluna():
    return mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


def dinheiro_coluna(*, nullable: bool = False):
    return mapped_column(Numeric(MONEY_PRECISION, MONEY_SCALE), nullable=nullable)


UUIDType = uuid.UUID
DateTimeType = datetime
DecimalType = Decimal
