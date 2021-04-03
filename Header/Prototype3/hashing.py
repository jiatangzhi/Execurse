import hashlib

def hash_password(username, password):
    '''Encrypts the password entered by the user by using their username
    as a salt and then uses the md5 algorithm
    Arguments:
        username(str): the username that the user has entered on signup
        password(str): the password the user entered on signup
    Returns:
        hashed_password(str): the encrypted password
    '''
    salted_password = password+username
    hashed_password = salted_password.encode("utf-8")
    hashed_password = hashlib.md5(hashed_password)
    hashed_password = hashed_password.hexdigest()
    
    return hashed_password

def check_password(username, password, password_hash):
    '''Checks that the password that the user has entered when logging in
    is the one stored in the database by encrypting the password the user
    entered and comparing it to the encrpyted password in the database.
    Arguments:
        username(str): the username that the user has entered when logging in
        password(str): the password the user entered when logging in
        password_hash(str): the encrypted password stored in the database
    Returns:
        True if the encrypted passwords match, False otherwise
    '''
    salted_password = password+username
    hashed_password = salted_password.encode("utf-8")
    hashed_password = hashlib.md5(hashed_password)
    hashed_password = hashed_password.hexdigest()
    
    if password_hash == hashed_password:
        return True
    else:
        return False