from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, LocalCreateUpdateMix)


class MinusKeywordsModel(Base, ActiveMix, LocalCreateUpdateMix):
    __tablename__ = "minus_keywords"

    id: Mapped[int] = mapped_column(primary_key=True)
    minus_subject_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("minus_keywords_subject.id"))

    minus_keyword: Mapped[str]
