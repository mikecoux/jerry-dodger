from models import session, Score

# Creates a score instance
def capture_score(new_score, user):
    new_score = Score(score = new_score, user_id = user.id)
    save_score(new_score)

# Saves score to score db
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

def get_last_score():
    return session.query(
        Score).order_by(
        Score.id.desc()).first()