from flask import session

def UserLogged():
    if 'email' in session:
        return True
    else:
        return False