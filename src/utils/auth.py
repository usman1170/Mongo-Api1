def validate_login_data(email, password):
    if email in ['', None] or password in ['', None]:
        return {"message":"Missing Email or Password"}
    return True