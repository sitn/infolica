from sqlalchemy import (
    Column,
    Index,
    Integer,
    BigInteger,
    Float,
    Text,
    Date,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)

from .meta import Base_mssql


class VBalance(Base_mssql):
    __tablename__ = 'v_Balance'
    __table_args__ = {'schema': 'dbo'}
    id = Column(Text, primary_key=True)
    ancien = Column(Text)
    nouveau = Column(Text)
    genre = Column(Integer)
    base = Column(Text)
    affaire = Column(Text)
