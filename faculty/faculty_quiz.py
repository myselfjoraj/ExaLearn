from flask import session, json, render_template, url_for, redirect, jsonify
from flask_login import current_user

from dao.main_dao import MainDAO
from misc import extras
from models.quiz import Quiz


def quiz_add(request, db):
    is_new = request.args.get('new')
    is_id = request.args.get('id')
    if is_new == 'true':
        session.pop("quiz_id")
    elif is_new == 'false' and is_id is not None:
        session['quiz_id'] = is_id

    if 'quiz_id' not in session:
        id = extras.getUUID()
        session['quiz_id'] = id
    else:
        id = session['quiz_id']
    if 'new_quiz_model' in session:
        try:
            json_dict = json.loads(session['new_quiz_model'])
            session.pop('new_quiz_model')
            quiz = Quiz.from_dict(json_dict)
            print(quiz.no)
            MainDAO(db).quiz_qn_list_add(current_user.email, id, json_dict)
        except Exception as e:
            print(e)

    category = MainDAO(db).category_list()
    qn_list = Quiz.parse_quiz(MainDAO(db).quiz_qn_list(current_user.email, id))
    name = None
    if qn_list is not None and isinstance(qn_list[0], str):
        name = qn_list[0]
        del qn_list[0]
    print(qn_list)
    return render_template('faculty-add-quiz.html', category=category, qn_list=qn_list, name=name, id=id)


def qn_submit(request):
    if request.method == 'POST':
        question = request.form.get('question')
        op_1 = request.form.get('op_1')
        op_2 = request.form.get('op_2')
        op_3 = request.form.get('op_3')
        op_4 = request.form.get('op_4')
        answer = request.form.get('answer')
        points = request.form.get('points')
        if answer == 'op_1':
            answer = op_1
        elif answer == 'op_2':
            answer = op_2
        elif answer == 'op_3':
            answer = op_3
        else:
            answer = op_4

        quiz = Quiz(0, question, points, op_1, op_2, op_3, op_4, answer)

        # print(f"Question: {question}")
        # print(f"Option 1: {op_1}")
        # print(f"Option 2: {op_2}")
        # print(f"Option 3: {op_3}")
        # print(f"Option 4: {op_4}")
        # print(f"Answer: {answer}")
        # print(f"Points: {points}")

        session['new_quiz_model'] = json.dumps(quiz.to_dict())

        return redirect(url_for("faculty_quiz_add"))


def submit_title(request, db):
    if request.method == 'POST':
        try:
            data = request.get_json()
            val = data.get('quiz_title')
            print(val)
            if val and 'quiz_id' in session:
                MainDAO(db).quiz_qn_list_add_name(current_user.email, session['quiz_id'], val)
            return jsonify({'message': 'Quiz title received successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
