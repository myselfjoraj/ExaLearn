import ast
import json
import os
import pprint

from flask import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import firebase_admin
from firebase_admin import db, storage
from werkzeug.utils import secure_filename

import misc.constants
from misc import extras
from models.contents import Contents
from models.faculty import Faculty
from models.quiz import Quiz
from models.section import Section
from models.user import User
from auth.login_system import LoginSystem
import misc.cred as mKey
from misc.extras import *
from routes import faculty_routes, faculty_main
from misc.constants import *
from dao.main_dao import *

app = Flask(__name__)
app.secret_key = mKey.SECRET_KEY

cred = firebase_admin.credentials.Certificate('cloud_key.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': mKey.DB_URL,
    'storageBucket': mKey.STORAGE_URL
})

# Get a reference to the storage service
bucket = storage.bucket()

# login manager initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'faculty_login'


@app.route("/reg")
def reg():
    ab = LoginSystem(db).login_user(encode_email("jorajonline@gmail.com"), "Joraj@01")
    print(ab.message)
    usr = ab.message
    with app.app_context():
        login_user(usr)
    return "reg"


# user registration page
@app.route("/register")
def register_page():
    if current_user.is_authenticated:
        return f"authenticated - {current_user.email_verified}"
    return "register page"


# user login page
@app.route("/login")
def login_page():
    return "login page"


# user base page
@app.route("/")
@login_required
def index_page():
    return "index page"


@app.route("/dashboard")
@login_required
def dashboard_page():
    return "dashboard page"


# user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'login_info')
    return redirect(url_for('login_page'))


# user loader for flask login
@login_manager.user_loader
def load_user(user_id):
    if 'user_dict' in session:
        user = User.from_dict(session['user_dict'])
        if user.email == user_id:
            return user
        else:
            session.pop('user_dict')
            return None
    elif 'fac_dict' in session:
        user = Faculty.from_dict(session['fac_dict'])
        if user.email == user_id:
            return user
        else:
            session.pop('fac_dict')
            return None
    return None


#######################################################################################################################

''' FACULTY LINKS'''


@app.route("/faculty", methods=['GET', 'POST'])
def faculty_login():
    msg = request.args.get('msg')
    if msg is not None:
        msg = msg.upper()
        if msg == SUCCESS:
            msg = "Account created successfully! Please login."
        elif msg == EMAIL_EXISTS:
            msg = "Account with same email id exists! Please login or click forget password to generate a new password!"
        return render_template('faculty-login.html', msg=msg, err=0)

    f_login = faculty_main.login(request, db)
    if f_login is None:
        return render_template('faculty-login.html')
    elif f_login.success:
        fac = f_login.message
        with app.app_context():
            login_user(fac)
        return redirect('/faculty/dashboard')
    elif not f_login.success:
        if f_login.message == EMPTY_FIELDS:
            msg = "One or more fields are empty"
        elif f_login.message == PASSWORD_ERROR:
            msg = "Incorrect Password!"
        elif f_login.message == USER_NOT_EXISTS:
            msg = "User with this email doesn't exists!"
        else:
            msg = f_login.message
        return render_template('faculty-login.html', msg=msg, err=1)

    return render_template('faculty-login.html')


@app.route("/faculty/register", methods=['GET', 'POST'])
def faculty_register():
    return faculty_routes.faculty_register(request, db, bucket)


@app.route("/faculty/forget-password")
def faculty_forget_password():
    return None


@app.route("/faculty/profile")
def faculty_profile():
    return render_template('faculty-profile.html')


@app.route("/faculty/my-profile")
def faculty_my_profile():
    return render_template('faculty-edit-profile.html')


@app.route("/faculty/dashboard")
@login_required
def faculty_dash():
    print(MainDAO(db).category_list())
    return render_template('faculty-dashboard.html', user=current_user, email=decode_email(current_user.email))


# COURSE
@app.route("/faculty/courses")
def faculty_course():
    return render_template('faculty-courses.html')


@app.route("/faculty/course/throw", methods=['GET', 'POST'])
def faculty_course_throw():
    return faculty_routes.faculty_course_throw(request, db)


@app.route("/faculty/courses/add")
def faculty_course_add():
    return faculty_routes.faculty_course_add(request, db)


@app.route('/faculty/courses/add/details', methods=['GET', 'POST'])
def faculty_course_add_title():
    return faculty_routes.faculty_course_add_title(request)


@app.route("/faculty/courses/add/section")
def faculty_course_add_section():
    return faculty_routes.faculty_course_add_section(request)


@app.route("/faculty/courses/add/section/content")
def faculty_course_add_section_content():
    return render_template("faculty-add-contents.html")


@app.route("/faculty/courses/add/section/quiz")
def faculty_course_add_section_quiz():
    quiz_list = extras.quiz_iterator(MainDAO(db).quiz_list(current_user.email))
    return render_template("faculty-add-course-quiz.html", quiz_list=quiz_list)


# quiz
@app.route("/faculty/quiz")
def faculty_quiz():
    quiz_list = extras.quiz_iterator(MainDAO(db).quiz_list(current_user.email))
    return render_template('faculty-quiz.html', quiz_list=quiz_list)


@app.route("/faculty/quiz/add")
def faculty_quiz_add():
    return faculty_routes.faculty_quiz_add(request, db)


@app.route("/faculty/quiz/add/qn")
def faculty_quiz_add_qn():
    return render_template('faculty-add-quiz-qn.html', )


@app.route('/faculty/quiz/add/qn/submit', methods=['GET', 'POST'])
def faculty_quiz_add_qn_submit():
    return faculty_routes.faculty_quiz_add_qn_submit(request)


@app.route('/faculty/quiz/add/qn/submit/title', methods=['GET', 'POST'])
def faculty_quiz_add_qn_submit_title():
    return faculty_routes.faculty_quiz_add_qn_submit_title(request, db)


@app.route('/faculty/quiz/delete', methods=['GET', 'POST'])
def faculty_quiz_delete():
    id = request.args.get('id')
    if id:
        MainDAO(db).quiz_delete(current_user.email, id)
        print("deleted successfully")
    return redirect(url_for("faculty_quiz"))


@app.route('/faculty/quiz/delete/qn', methods=['GET', 'POST'])
def faculty_quiz_delete_qn():
    id = request.args.get('id')
    if id:
        MainDAO(db).quiz_delete(current_user.email, id)
        print("deleted successfully")
    return redirect(url_for("faculty_quiz"))


@app.route("/faculty/stud")
def faculty_stud():
    return render_template('faculty-students.html')


@app.route("/faculty/leaderboard")
def faculty_leaderboard():
    return render_template('faculty-leaderboard.html')


# community
@app.route("/faculty/community")
def faculty_community():
    return render_template('faculty-discussions.html')


@app.route("/faculty/community/view")
def faculty_community_view():
    return render_template('faculty-discussions-view.html')


@app.route("/faculty/community/ask")
def faculty_community_ask():
    return render_template('faculty-discussions-ask.html')


@app.route("/faculty/ai")
def faculty_gpt():
    return render_template('faculty-ai.html')


@app.route("/video-upload", methods=['GET', 'POST'])
def video_upload():
    if 'videoFile' not in request.files:
        return jsonify({'error': 'No video file part in the request'}), 400

    video_file = request.files['videoFile']
    if video_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    print("started process")
    filename = secure_filename(video_file.filename)
    file_path = os.path.join('/tmp', filename)
    video_file.save(file_path)

    if 'course_id' in session:
        id = session['course_id']
    else:
        id = extras.getUUID()

    folder_name = "courses/" + current_user.email + "/" + id

    blob = bucket.blob(f'{folder_name}/{filename}')
    blob.upload_from_filename(file_path)
    blob.make_public()

    print(blob.public_url)

    return jsonify({'message': 'File uploaded successfully', 'url': blob.public_url}), 200


@app.route("/thumb-upload", methods=['GET', 'POST'])
def thumb_upload():
    if 'imageFile' not in request.files:
        return jsonify({'error': 'No video file part in the request'}), 400

    image_file = request.files['imageFile']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    print("started process")
    filename = secure_filename(image_file.filename)
    file_path = os.path.join('/tmp', filename)
    image_file.save(file_path)

    if 'course_id' in session:
        id = session['course_id']
    else:
        id = extras.getUUID()

    folder_name = "courses/" + current_user.email + "/" + id + "/thumb"

    blob = bucket.blob(f'{folder_name}/{filename}')
    blob.upload_from_filename(file_path)
    blob.make_public()

    print(blob.public_url)

    return jsonify({'message': 'File uploaded successfully', 'url': blob.public_url}), 200


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
