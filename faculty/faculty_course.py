import time

from flask import session, json, render_template, jsonify
from flask_login import current_user

from dao.main_dao import MainDAO
from misc import extras
from models.contents import Contents
from models.course import Course
from models.section import Section


def main(request, db):
    is_new = request.args.get('new')
    is_id = request.args.get('id')
    section = request.args.get('list')
    title = request.args.get('title')
    refresh_list = request.args.get("refresh")
    quiz_title = request.args.get('quiz_title')
    quiz_id = request.args.get('quiz_id')
    if is_new == 'true':
        extras.session_pop("course_id")
        extras.session_pop('course_name')
        extras.session_pop('course_desc')
        extras.session_pop('course_price')
        extras.session_pop('course_cat')
        extras.session_pop('section_list')
        extras.session_pop('course_thumb')
    elif is_new == 'false' and is_id is not None:
        session['course_id'] = is_id

    category = MainDAO(db).category_list()

    if 'course_id' not in session:
        id = extras.getUUID()
        session['course_id'] = id
    else:
        id = session['course_id']

    if 'course_name' in session:
        name = session['course_name']
    else:
        name = None

    if 'course_desc' in session:
        desc = session['course_desc']
    else:
        desc = None

    if 'course_price' in session:
        price = session['course_price']
    else:
        price = 0
        session['course_price'] = 0

    if 'course_cat' in session:
        cat = session['course_cat']
    else:
        cat = category[0]
    print(cat)

    if 'course_thumb' in session:
        thumb = session['course_thumb']
    else:
        thumb = None

    section_list = []
    if 'section_list' in session:
        section_list = session['section_list']

    if section is not None:
        section_model = Section(1, title, section).to_dict()
        section_list.append(section_model)
        session['section_list'] = section_list

    if quiz_title is not None and quiz_id is not None:
        # m = Contents(2, quiz_title, quiz_id, "30").to_dict()
        m = f'[{{"id": 2, "title": "{quiz_title}", "desc": "{quiz_id}", "duration": 30, "url": "url"}}]'
        sec_model = Section(2, quiz_title, m).to_dict()
        if sec_model not in section_list:
            section_list.append(sec_model)
        else:
            print("already exists!")
        session['section_list'] = section_list

    display_list = []
    if refresh_list is not None and len(refresh_list) > 0:
        refresh_list = json.loads(refresh_list)
        for ref in refresh_list:
            r = Section.from_dict(ref)
            display_list.append(r.to_dict())
    else:
        for sec in section_list:
            if isinstance(sec, dict):
                s = Section.from_dict(sec)
            elif isinstance(sec, str):
                sec_dict = json.loads(sec)  # Convert string to dictionary
                s = Section.from_dict(sec_dict)
            else:
                continue  # Skip if not a dictionary or string
            if isinstance(s.content, str):
                s.content = json.loads(s.content)
            display_list.append(s.to_dict())

    session['section_list'] = display_list

    print(len(display_list))

    return render_template("faculty-add-course.html", name=name, desc=desc, price=price, cat=cat, category=category,
                           section_list=display_list, id=id, thumb=thumb)


def edit(request, db, course):
    is_new = request.args.get('new')
    section = request.args.get('list')
    title = request.args.get('title')
    refresh_list = request.args.get("refresh")
    quiz_title = request.args.get('quiz_title')
    quiz_id = request.args.get('quiz_id')
    if is_new == 'true':
        extras.session_pop("course_id")
        extras.session_pop('course_name')
        extras.session_pop('course_desc')
        extras.session_pop('course_price')
        extras.session_pop('course_cat')
        extras.session_pop('section_list')
        extras.session_pop('course_thumb')

    category = MainDAO(db).category_list()

    if 'course_id' not in session:
        id = course.id
        session['course_id'] = id
    else:
        id = session['course_id']

    if 'course_name' in session:
        name = session['course_name']
    else:
        name = course.title
        session['course_name'] = name

    if 'course_desc' in session:
        desc = session['course_desc']
    else:
        desc = course.description
        session['course_desc'] = desc

    if 'course_price' in session:
        price = session['course_price']
    else:
        price = course.price
        session['course_price'] = price

    if 'course_cat' in session:
        cat = session['course_cat']
    else:
        cat = course.category
        session['course_cat'] = cat

    if 'course_thumb' in session:
        thumb = session['course_thumb']
    else:
        thumb = course.thumbnail
        session['course_thumb'] = thumb

    print(cat)

    section_list = []
    if 'section_list' in session:
        section_list = session['section_list']

    if section is not None:
        section_model = Section(1, title, section).to_dict()
        section_list.append(section_model)
        session['section_list'] = section_list

    if course.section is not None:
        for sec in course.section:
            section_list.append(sec)
            session['section_list'] = section_list

    if quiz_title is not None and quiz_id is not None:
        # m = Contents(2, quiz_title, quiz_id, "30").to_dict()
        m = f'[{{"id": 2, "title": "{quiz_title}", "desc": "{quiz_id}", "duration": 30, "url": "url"}}]'
        sec_model = Section(2, quiz_title, m).to_dict()
        if sec_model not in section_list:
            section_list.append(sec_model)
        else:
            print("already exists!")
        session['section_list'] = section_list

    display_list = []
    if refresh_list is not None and len(refresh_list) > 0:
        refresh_list = json.loads(refresh_list)
        for ref in refresh_list:
            r = Section.from_dict(ref)
            display_list.append(r.to_dict())
    else:
        for sec in section_list:
            if isinstance(sec, dict):
                s = Section.from_dict(sec)
            elif isinstance(sec, str):
                sec_dict = json.loads(sec)  # Convert string to dictionary
                s = Section.from_dict(sec_dict)
            else:
                continue  # Skip if not a dictionary or string
            if isinstance(s.content, str):
                s.content = json.loads(s.content)
            display_list.append(s.to_dict())

    session['section_list'] = display_list

    print(len(display_list))

    return render_template("faculty-add-course.html", name=name, desc=desc, price=price, cat=cat, category=category,
                           section_list=display_list, id=id, thumb=thumb)


def add_title(request):
    if request.method == 'POST':
        try:
            data = request.get_json()
            title = data.get('course_title')
            desc = data.get('course_desc')
            cat = data.get('course_category')
            price = data.get('course_price')

            if 'course_id' in session:
                if title is not None:
                    session['course_name'] = title
                if desc is not None:
                    session['course_desc'] = desc
                if price is not None:
                    session['course_price'] = price
                if cat is not None:
                    session['course_cat'] = cat

            return jsonify({'message': 'Course title received successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 400


def add_section(request):
    title = request.args.get('courseTitle')
    desc = request.args.get('courseDescription')
    duration = request.args.get('duration')
    url = request.args.get('videoFile')
    is_new = request.args.get('new')
    if is_new is not None and is_new == 'true':
        extras.session_pop('content_list')
    content_list = []
    if 'content_list' in session:
        content_list = session['content_list']
    if title is not None and desc is not None and duration is not None:
        content = Contents(1, title, desc, duration, url).to_dict()
        content_list.append(content)
        session['content_list'] = content_list
    print(content_list)
    return render_template("faculty-add-section.html", content_list=content_list)


def throw(request, db):
    if request.method == 'POST':
        url = request.form['url']
        s_list = request.form['list']
        id = session['course_id']
        name = session['course_name']
        desc = session['course_desc']
        price = session['course_price']
        cat = session['course_cat']
        if not cat:
            cat = 'java'
        duration = extras.calculate_total_duration(s_list)
        course = Course(id, name, desc, cat, price, duration, url, json.loads(s_list), current_user.email, time.time())
        MainDAO(db).course_add(id, course.to_dict())
        return jsonify({'message': 'success'}), 200


def course_list(db):
    c_list = MainDAO(db).my_course_list()
    my_course_list = []
    for key, val in c_list.items():
        k = key
        course = Course.from_dict(MainDAO(db).course_list_by_id(k))
        my_course_list.append(extras.course_iterator(course))
    return my_course_list
