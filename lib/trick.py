from models import session, Trick

def capture_tricks(steeze_inputs, user, game):
    for steeze in steeze_inputs:
        new_trick = Trick(steeze = steeze, user_id = user.id, game_id = game.id)
        save_tricks(new_trick)

def save_tricks(trick):
    session.add(trick)
    session.commit()