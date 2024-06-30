from flask import *
import firebase_admin
from firebase_admin import auth
import helper.user_auth as mAuth
from auth.login_system import LoginSystem
import misc.cred as mKey

app = Flask(__name__)

app.secret_key = mKey.SECRET_KEY

cred = firebase_admin.credentials.Certificate('cloud_key.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': mKey.DB_URL,
    'storageURL': mKey.STORAGE_URL
})

a = LoginSystem.register_user("joraj2net@gmail.com", "aabccddeeee")
print(str(a.success) + " " + a.message)

if __name__ == "__main__":
    app.run(debug=True)
