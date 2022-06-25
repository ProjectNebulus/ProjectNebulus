from werkzeug.security import check_password_hash, generate_password_hash


def hash256(password):
    hashed = generate_password_hash(password)
    return str(hashed)
print(hash256('12345*'))


def valid_password(hashed, unhashed):
    # print(
    #     f"check_password_hash('{hashed}', '{unhashed}' = {check_password_hash(hashed, unhashed)}"
    # )
    return check_password_hash(hashed, unhashed)
