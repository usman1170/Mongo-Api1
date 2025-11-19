from views.auth_view import Register, Login
from config import api


baseUrl = "/api/auth"

api.add_resource(Register, f"{baseUrl}/register")
api.add_resource(Login, f"{baseUrl}/login")