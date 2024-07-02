import uuid

EMAIL_EXISTS = "EMAIL_EXISTS"

SUCCESS = 'SUCCESS'


def getUUID():
    return str(uuid.uuid4()).replace("-", "")
