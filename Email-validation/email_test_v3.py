#part of incomplete validation system
def send_code(receiver_email,code):
    import smtplib, ssl

#https://realpython.com/python-send-email/

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "groupvtest@gmail.com"  # Enter your address
    password = "K67Lx6YH_MZqc8A" #password for your account
    message = ("""\
Subject: Account Verification

your account verification code is as follows

verification code: """ + code +
"""

if you beleive you have received this code in error, please contact someone about it""")

#sending email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except:
        print("email not valid")
