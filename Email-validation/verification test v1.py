#requires acccess to email test v3
import random
import string
import email_test_v3

code = ""
possibles = string.ascii_letters + string.digits
possibles = possibles.replace("o","")
possibles = possibles.replace("O","")
possibles = possibles.replace("i","")
possibles = possibles.replace("I","")
possibles = possibles.replace("l","")

for i in range(8):
    code = code +(random.choice(possibles))
    

print(possibles)
print(code)

email_test_v3.send_code("groupvtest@gmail.com",code)
