from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine("mysql+pymysql://root:Rexema_4082@127.0.0.1:3306/async_chat", echo=True)
Base = declarative_base()

class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    login = Column(String(250), nullable=False)
    port = Column(String(250), nullable=False)
    history = relationship('ClientHistory', backref='client', uselist=False)
   


class ClientHistory(Base):
    __tablename__ = 'client_history'

    id = Column(Integer, primary_key=True)
    time_of_login = Column(DateTime)
    ip_address = Column(String(250), nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), unique=True)
   


Base.metadata.create_all(engine)