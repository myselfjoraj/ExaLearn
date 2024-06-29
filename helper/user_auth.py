from firebase_admin import auth
from models.user import User


def create_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            email_verified=False
        )
        print(user.uid)
        return None
    except Exception as e:
        return str(e)


def get_user(uid):
    try:
        user = auth.get_user(uid)
        return User(user.uid, user.email)
    except Exception as e:
        return str(e)


def update_user(uid, password=None):
    try:
        user = auth.update_user(
            uid,
            password=password
        )
        return User(user.uid, user.email, user.display_name, user.phone_number, user.photo_url), None
    except Exception as e:
        return str(e)


def delete_user(uid):
    try:
        auth.delete_user(uid)
        return True, None
    except Exception as e:
        return False, str(e)


def verify_id_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token, None
    except Exception as e:
        return None, str(e)
