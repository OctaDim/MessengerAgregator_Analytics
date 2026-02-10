from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, LocalCreateUpdateMix)


class PlusKeywordsSubjectModel(Base, ActiveMix, LocalCreateUpdateMix):
    __tablename__ = "plus_keywords_subject"

    id: Mapped[int] = mapped_column(primary_key=True)

    plus_subject: Mapped[Optional[str]] = mapped_column(String(100))



class MinusKeywordsSubjectModel(Base, ActiveMix, LocalCreateUpdateMix):
    __tablename__ = "minus_keywords_subject"

    id: Mapped[int] = mapped_column(primary_key=True)

    minus_subject: Mapped[str] = mapped_column(String(100))
