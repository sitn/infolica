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


class VImmeubles(Base_mssql):
    __tablename__ = 'v_Immeubles'
    __table_args__ = {'schema': 'dbo'}
    numcom = Column(Integer)
    fkimm = Column(Text, primary_key=True)
