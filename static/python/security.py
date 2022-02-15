from werkzeug.security import check_password_hash, generate_password_hash


def hash256(password):
    hashed = generate_password_hash(password)
    return str(hashed)


def valid_password(hashed, unhashed):
    if check_password_hash(hashed, unhashed):
        return True
    return False
