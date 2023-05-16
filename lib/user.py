from models import session, Base, engine, User
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def save_user(user):
    session.add(user)
    session.commit()
    print(user)

def get_all_users():
    return session.query(User).all()

def get_user_by_name(name):
    return session.query(User).filter(User.username == name).first()