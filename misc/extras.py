import random
import re


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
