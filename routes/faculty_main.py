import misc.extras
from auth.login_system import LoginSystem
from helper.crypt_helper import Crypt
from helper.firebase_helper import FirebaseHelper
from misc import constants, extras
from models.except_control import ExceptControl
from models.faculty import Faculty


def register(request, db, bucket):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        file = request.files['file']
        if name is None and email is None and password is None and phone is None and file is None:
            return ExceptControl(False, constants.EMPTY_FIELDS)
        elif not extras.is_valid_email(email):
            return ExceptControl(False, constants.INCORRECT_EMAIL)
        elif len(password) < 8:
            return ExceptControl(False, constants.PASSWORD_LENGTH_DOWN)
        else:
            email = extras.encode_email(email)
            photo_url = FirebaseHelper.upload_file(bucket, file, "profile_image", email)
            user = Faculty(email, Crypt().encrypt(password), name, False, extras.generate_otp(), phone, photo_url)
            print(user.to_dict())
            return LoginSystem(db).register_faculty(user)


def login(request, db):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email is None and password is None:
            return ExceptControl(False, constants.EMPTY_FIELDS)
        else:
            email = misc.extras.encode_email(email)
            return LoginSystem(db).login_faculty(email, password)

