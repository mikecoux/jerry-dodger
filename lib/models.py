from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///jerry-dodger.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(), index=True)
    init_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"User #{self.id}: " \
            + f"{self.username}, " \
            + f"{self.init_date}"