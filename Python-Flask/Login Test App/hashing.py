import hashlib

def hash_password(username, password):
    salted_password = password+username
    hashed_password = salted_password.encode("utf-8")
    hashed_password = hashlib.md5(hashed_password)
    hashed_password = hashed_password.hexdigest()
    
    return hashed_password

def check_password(username, password, password_hash):
    salted_password = password+username
    hashed_password = salted_password.encode("utf-8")
    hashed_password = hashlib.md5(hashed_password)
    hashed_password = hashed_password.hexdigest()
    
    if password_hash == hashed_password:
        return True
    else:
        return False