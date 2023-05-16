from lib.models import session, Base, engine
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def save_user(user):
    session.add(user)
    session.commit()
    print(user)
