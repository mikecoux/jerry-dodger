from models import session, Score
from sqlalchemy import desc

def save_score(score):
    session.add(score)
    session.commit()
    print(score)

# Return the top 5 scores for a given user
def get_top_scores(id):
    return session.query(
        Score).filter(
        Score.user_id == id).order_by(
        Score.score.desc()).limit(
        5).all()