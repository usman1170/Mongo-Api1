from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from config import mongoDBManager
from schemas.user_model import UserModel
from src.db.user import Users
from src.utils.auth import validate_login_data
from werkzeug.security import check_password_hash,generate_password_hash
 
 
        
class Register(Resource):
    def post(self):
        try:
            data = request.get_json()
            
            user_model = UserModel(
                name=data.get("name"),
                email=data.get("email"),
                password=generate_password_hash(data.get("password")),
                role=data.get("role"),
                phone=data.get("phone"),
            )
            if Users.get_user(email=user_model.email):
                return {"message": "Email already exists", "type" : "email"}, 409
            user = Users.add_user(user_model)
            if not user:
                return {"error":"User creation failed"},500
            return {"message":"User created successfully"}, 201
        except ValidationError as e:
            return {"Error": e.errors()}, 400
        except Exception as e:
            print(e)
            return {"Error" : "Something wents wrong"},500
        
        
class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")
            valid_response =  validate_login_data(email, password)
            if valid_response != True:
                return valid_response,400
            user = Users.get_user(email = email)
            if not user:
                return {"Error" : "User not found"},404
            if check_password_hash(user.get("password"), password) == False: 
                return {"Error" : "Invalid Credentials"},401
            access_token = create_access_token(identity=str(user.get("_id")))
            refresh_token = create_refresh_token(identity=str(user.get("_id")))
            user_resp = {
                "id":str(user.get("_id")),
                "name":user.get("name"),
                "email":user.get("email"),
                "role":user.get("role"),
                "phone":user.get("phone"),
                "created_at":user.get("created_at"),
                "access_token":access_token,
                "refresh_token":refresh_token,
            }
            return {"data":user_resp}, 200
        except Exception as e:
            print(e)
            return {"Error" : f"Something wents wrong: {e}"},500