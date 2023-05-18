from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

engine = create_engine('sqlite:///jerry_dodger.db')
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(), index=True)
    init_date = Column(DateTime(), default=datetime.now())
    scores = relationship("Score", backref="users")
    tricks = relationship("Trick", backref="users")

    def __repr__(self):
        return f"USER #{self.id} - " \
            + f"username: {self.username}"
    
class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    game_date = Column(DateTime(), default=datetime.now())
    user_id = Column(Integer(), ForeignKey('users.id'))
    tricks = relationship("Trick", backref="scores")

    def __repr__(self):
        return f"GAME #{self.id} - " \
        + f"score: {self.score}, " \
        + f"user ID: {self.user_id}"
    
class Trick(Base):
    __tablename__ = 'tricks'

    id = Column(Integer(), primary_key=True)
    steeze = Column(String())
    user_id = Column(Integer(), ForeignKey('users.id'))
    game_id = Column(Integer(), ForeignKey('scores.id'))