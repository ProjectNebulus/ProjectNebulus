from werkzeug.security import generate_password_hash, check_password_hash


def hash256(password):
    hashed = generate_password_hash(password)
    return str(hashed)


def valid_password(hashed, unhashed):
    return check_password_hash(hashed, unhashed)
