from sqlalchemy import Column, Integer, String
from .database import Base

class Voucher(Base):
    __tablename__ = "vouchers"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, unique=True, index=True)
    brand = Column(String)
    amount = Column(Integer)

class VoucherSequence(Base):
    __tablename__ = "voucher_sequences"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    amount = Column(Integer)
    last_code = Column(Integer)
