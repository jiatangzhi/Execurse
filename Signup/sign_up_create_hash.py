import hashlib

def login(username, password):

    x = password + username
    
    xUtf8 = x.encode("utf-8")
    
    xHash = hashlib.md5( xUtf8 )
    
    xHex = xHash.hexdigest()

    return xHex
