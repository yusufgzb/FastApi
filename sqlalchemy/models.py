
from sqlalchemy import Boolean, Column, Integer, String
from db import Base


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    complate = Column(Boolean,default=False)
