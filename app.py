from flask import *
import firebase_admin
from firebase_admin import auth
import helper.user_auth as mAuth
from auth.login_system import LoginSystem

app = Flask(__name__)
app.secret_key =

cred = firebase_admin.credentials.Certificate('cloud_key.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://exalearn-77758-default-rtdb.asia-southeast1.firebasedatabase.app"
})

a = LoginSystem.register_user("joraj2net@gmail.com", "aabccddeeee")
print(str(a.success)+" "+a.message)

if __name__ == "__main__":
    app.run(debug=True)
