from flask import render_template, redirect

from dao.main_dao import MainDAO
from faculty import faculty_course, faculty_quiz
from misc.constants import *
from models.course import Course

from routes import faculty_main


def faculty_register(request, db, bucket):
    f_reg = faculty_main.register(request, db, bucket)
    if f_reg is None:
        return render_template('faculty-signup.html')
    elif f_reg.success and f_reg.message == SUCCESS:
        return redirect("/faculty?msg=success")
    elif not f_reg.success:
        msg = None
        if f_reg.message == EMPTY_FIELDS:
            msg = "One or more fields are empty"
        elif f_reg.message == INCORRECT_EMAIL:
            msg = "Please enter a valid email address"
        elif f_reg.message == PASSWORD_LENGTH_DOWN:
            msg = "Please enter a password with more than eight characters"
        elif f_reg.message == EMAIL_EXISTS:
            return redirect("/faculty?msg=email_exists")
        else:
            msg = str(f_reg.message)
        return render_template('faculty-signup.html', msg=msg)
    else:
        return render_template('faculty-signup.html')


def faculty_course_list(request, db):
    course_list = faculty_course.course_list(db)
    free = []
    paid = []
    for c in course_list:
        if str(c.price) == "0":
            free.append(c)
        else:
            paid.append(c)
    if len(free) == 0:
        free = None
    if len(paid) == 0:
        paid = None
    return render_template('faculty-courses.html', free=free, paid=paid)


def faculty_course_edit(request, db):
    id = request.args.get("id")
    course = Course.from_dict(MainDAO(db).course_list_by_id(id))
    return faculty_course.edit(request, db, course)


def faculty_course_add(request, db):
    return faculty_course.main(request, db)


def faculty_course_throw(request, db):
    return faculty_course.throw(request, db)


def faculty_course_add_title(request):
    return faculty_course.add_title(request)


def faculty_course_add_section(request):
    return faculty_course.add_section(request)


def faculty_quiz_add(request, db):
    return faculty_quiz.quiz_add(request, db)


def faculty_quiz_add_qn_submit(request):
    return faculty_quiz.qn_submit(request)


def faculty_quiz_add_qn_submit_title(request, db):
    return faculty_quiz.submit_title(request, db)
