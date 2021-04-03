#requires acccess to email test v3

def create_code():
    '''Creates code for verification
    Arguements:
        Nothing
    Returns:
        code(string): code used in verification, length 8
    '''
    import random
    import string
    code = ""
    possibles = string.ascii_letters + string.digits
    possibles = possibles.replace("o","")
    possibles = possibles.replace("O","")
    possibles = possibles.replace("i","")
    possibles = possibles.replace("I","")
    possibles = possibles.replace("l","")

    for i in range(8):
        code = code +(random.choice(possibles))

    return code
    
