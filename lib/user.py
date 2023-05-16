# from sqlalchemy.orm import sessionmaker
from lib.models import session

# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()


def save(user):
    session.add(user)
    session.commit()
    print(user)
