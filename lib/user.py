from models import session, User

def capture_user(new_username):
    if new_username in [user.username for user in get_all_users()]:
        return get_user_by_name(new_username)
    else:
        new_user = User(username = new_username)
        save_user(new_user)
        return new_user

def save_user(user):
    session.add(user)
    session.commit()
    print(user)

def get_all_users():
    return session.query(User).all()

def get_user_by_name(name):
    return session.query(User).filter(User.username == name).first()