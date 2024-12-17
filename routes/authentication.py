from views.auth_view import AuthView, AuthView, Login
from config import app, api
from flask import request


baseUrl = "/api/auth"

api.add_resource(AuthView, f"{baseUrl}/register")
api.add_resource(Login, f"{baseUrl}/login")