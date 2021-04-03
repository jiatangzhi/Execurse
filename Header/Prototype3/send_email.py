def send_code(receiver_email,code):
    import smtplib, ssl
    '''send an email containing a code for verification
    Arguements:
        receiver_email(string): email of user
        code(string): code for validation
    Returns:
        Nothing
    '''

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "execursevalidation@gmail.com"  # project email address
    password = "K67Lx6YH_MZqc8A" #password for project email account
    message = ("""\
Subject: Account Verification

your account verification code is as follows

verification code: """ + code +
"""

if you believe you have received this code in error, please ignore this email""")

#sending email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except:
        print("email not valid")
