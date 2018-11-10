nono = " "
def verify_password(password, verify):

    if len(password) == 0:
        password_error = "Please give a password"
        tf = False
        return password_error

    elif len(password) < 3:
        password_error = "Your password is too short!"
        tf = False
        return password_error
                                                       #Checks password validity
    elif len(password) > 20:
        password_error = "Your password is too long!"
        tf = False
        return password_error

    elif nono in password:
        password_error = "Sorry, spaces aren't allowed in the password!"
        tf = False
        return password_error

    elif password != verify:                      #Verify password validity check
        password_error = "Passwords do not match!"
        tf = False
        return password_error
    else:
        return True

def verify_email(email):
    at_1 = "@"
    domain1 =".com"
    domain2 =".net"
    domain3 =".gov"
    domain4 =".org"

    if not email:
        email_error = "Pease give a valid email address"
        return email_error

    elif len(email) > 35:
        email_error = "I'm sorry, that email address is too long!"
        return email_error

    elif len(email) < 3:
        email_error = "I'm sorry that email is too short!"
        return email_error
                                                                       # Email validation
    elif at_1 not in email:
        email_error = "Not a valid email"
        return email_error

    elif domain1 not in email and domain2 not in email and domain3 not in email and domain4 not in email:
        email_error = "Not a valid email"
        return email_error

    elif nono in email:
        email_error = "Please...no spaces in the email address"
        return email_error

    else:
        return True
