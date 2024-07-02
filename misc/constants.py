import uuid

EMAIL_EXISTS = "EMAIL_EXISTS"

USER_NOT_EXISTS = "USER_NOT_EXISTS"

PASSWORD_ERROR = "PASSWORD_ERROR"


SUCCESS = 'SUCCESS'


def getUUID():
    return str(uuid.uuid4()).replace("-", "")
