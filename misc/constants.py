import uuid

EMAIL_EXISTS = "EMAIL_EXISTS"

USER_NOT_EXISTS = "USER_NOT_EXISTS"

PASSWORD_ERROR = "PASSWORD_ERROR"

PASSWORD_LENGTH_DOWN = "PASSWORD_LENGTH_DOWN"

EMPTY_FIELDS = "EMPTY_FIELDS"

INCORRECT_EMAIL = "INCORRECT_EMAIL"

SUCCESS = 'SUCCESS'


def getUUID():
    return str(uuid.uuid4()).replace("-", "")
