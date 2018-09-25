import re


def validate_email(email):
    if not isinstance(email, str):
        return False
    if len(email) <= 7:
        return False
    ans = re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email)
    if ans is None:
        return False
    return True


def validate_password(password):
    if not isinstance(str, password):
        return False
    ans = re.match(r"(?=.*[A-Za-z0-9])(?=.*[A-Z])(?=.*\d)(?=.*[#$^+=!*()@%&]).{6,12}", password)
    if ans is None:
        return False
    return True


def validate_username(username):
    if not isinstance(username, str):
        return False
    if len(username) < 6 or len(username) > 12:
        return False
    else:
        ans = re.match(r'^[a-z|\s]+$', username)
        if ans is None:
            return False
        return True
def empty(x):
    return len(x.strip()) == 0
