def encode_email(email):
    return str(email).replace(".", "_-")


def decode_email(email):
    return str(email).replace( "_-",".")
