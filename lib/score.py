from lib.models import session

def save_score(score):
    session.add(score)
    session.commit()
    print(score)