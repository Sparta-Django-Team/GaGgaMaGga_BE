import re


def password_validator(password):
    password_validation = (r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,16}")
    
    if not re.search(password_validation, str(password)):
        return True
    return False


def password_pattern(password):
    password_pattern = r"(.)\1+\1"
    
    if re.search(password_pattern, str(password)):
        return True
    return False


def username_validator(username):
    username_validations = r"^[A-Za-z0-9]{6,20}$"
    
    if not re.search(username_validations, str(username)):
        return True
    return False


def nickname_validator(nickname):
    nickname_validation = r"^[A-Za-z가-힣0-9]{3,10}$"
    
    if not re.search(nickname_validation, str(nickname)):
        return True
    return False