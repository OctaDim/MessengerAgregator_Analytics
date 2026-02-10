from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, LocalCreateUpdateMix)


class PlusKeywordsModel(Base, ActiveMix, LocalCreateUpdateMix):
    __tablename__ = "plus_keywords"

    id: Mapped[int] = mapped_column(primary_key=True)
    plus_subject_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("plus_keywords_subject.id"))

    plus_keyword: Mapped[str]
