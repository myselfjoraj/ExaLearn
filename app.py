from flask import *
import firebase_admin
from firebase_admin import auth
import helper.user_auth as mAuth

cred = firebase_admin.credentials.Certificate('./misc/service.json')

firebase_admin.initialize_app(cred, {
  'databaseURL': "https://exalearn-77758-default-rtdb.asia-southeast1.firebasedatabase.app"
})


# user = auth.create_user(
#     email='user@example.com',
#     email_verified=False,
#     phone_number='+918086786159',
#     password='password',
#     display_name='John Doe',
#     photo_url='https://buffer.com/library/content/images/size/w1200/2023/10/free-images.jpg',
#     disabled=False
# )

ab = mAuth.create_user("hi2oo@email.com","aabccddeeee")
print(ab)
# print('Successfully created new user: {0}'.format(user.uid))
# Get a reference to the database
