from lib.models import session

def save(user):
    session.add(user)
    session.commit()
    print(user)
