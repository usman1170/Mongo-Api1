from flask_restful import Resource
from flask import request
from config import mongoDBManager
from src.db.user import Users
 
UserCol = mongoDBManager.users

        
class AuthView(Resource):
    def post(self):
        try:
            data = request.get_json()
            response, status_code =Users.add_user(data)
            return response, status_code
        except Exception as e:
            return {"Error" : "Something wents wrong"},500
        
class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            response, status_code = Users.get_user(data)
            return response, status_code
        except Exception as e:
            print(e)
            return {"Error" : "Something wents wrong"},500