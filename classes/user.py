from sqlalchemy import (Index, Column, Integer, String, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    Index('index_name', 'username')

    id = Column(Integer(), primary_key=True)
    username = Column(String())
    init_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"User #{self.id}: " \
            + f"{self.username}, " \
            + f"{self.init_date}"