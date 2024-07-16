import json
import random
import re
import uuid
from datetime import datetime

from flask import session

from models.contents import Contents
from models.quiz import Quiz
from models.section import Section


def getUUID():
    return str(uuid.uuid4()).replace("-", "")


def get_short_uuid():
    full_uuid = uuid.uuid4()
    uuid_hex = full_uuid.hex
    short_uuid = uuid_hex[:7]
    return short_uuid


def encode_email(email):
    return str(email).replace(".", "_-")


def decode_email(email):
    return str(email).replace("_-", ".")


def generate_otp():
    return random.randint(100000, 999999)


def is_valid_email(email):
    if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email):
        return True
    else:
        return False


def session_pop(id):
    if id in session:
        session.pop(id)


def quiz_iterator(data):
    list1 = []
    if data is None:
        return list1
    for quiz_id, quiz_data in data.items():
        quiz_name = quiz_data.get('name')
        if quiz_name is None:
            quiz_name = "Untitled"
        i = 0
        point = 0
        for question_id, question_data in quiz_data.items():
            if question_id != 'name':
                i += 1
                points = question_data.get('points')
                point += int(points)

        list2 = [quiz_id, quiz_name, i, point]
        list1.append(list2)
    return list1


def course_iterator(course):
    section = course.section
    sections = []
    for data in section:
        sec = Section.from_dict(data)
        contents = []
        for con in sec.content:
            cont = Contents.from_dict(con)
            contents.append(cont)
        sec.content = contents
        sections.append(sec)
    course.section = sections
    course.duration = convert_minutes_to_hours(course.duration)
    return course


def calculate_total_duration(section_list):
    total_duration = 0
    section_list = json.loads(section_list)
    for section in section_list:
        if isinstance(section, dict) and "content" in section:
            for content_item in section["content"]:
                if isinstance(content_item, dict) and "duration" in content_item:
                    total_duration += int(content_item["duration"])
                else:
                    print(f"ignoring: {content_item}")
        else:
            print(f"ignoring: {section}")
    return total_duration


def convert_minutes_to_hours(minutes):
    if isinstance(minutes, str):
        minutes = int(minutes)
    hours = minutes // 60
    remaining_minutes = minutes % 60

    return f"{hours} h {remaining_minutes} min"


def parse_timestamp(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    formatted_date = dt_object.strftime('%d %b %Y')  # dd MMM yyyy
    return formatted_date
