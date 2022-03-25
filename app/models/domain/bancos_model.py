from sqlalchemy import Column, String, Integer

from app.db.base import Base


class Bancos_Model(Base):
    __tablename__ = "app_bancos"

    id = Column(Integer, primary_key=True)
    cod = Column(Integer, unique=True, index=True)
    banco = Column(String)
