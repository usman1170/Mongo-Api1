from flask_jwt_extended import create_access_token, create_refresh_token
from config import mongoDBManager
from schemas.user_model import UserModel
from pydantic import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash



UserCol = mongoDBManager.users
class Users():
    def __init__(self):
        pass
    
    
    @staticmethod
    def add_user(data):
        try:
            user_data = UserModel(
                name=data.get("name"),
                email=data.get("email"),
                password=generate_password_hash(data.get("password")),
                role=data.get("role"),
                phone=data.get("phone"),
            )
            check_user = UserCol.find_one({"email":user_data.email})
            if check_user:
                return {"Error": f"User already exists"}, 400
            UserCol.insert_one(user_data.dict())
            return {"message" : "User Created Successfully"}, 201
        except ValidationError as e:
            return {"Error": e.errors()}, 400
        
        except Exception as e:
            return {"Error":f"Something wents wrong : {e}"}, 500
        
    
    @staticmethod
    def get_user(data):
        try:    
            email = data.get("email")
            password = data.get("password")
            
            user = UserCol.find_one({"email":email})
            if not user:
                return {"Error":"User not found"},404
            if check_password_hash(user.get("password"), password) == False:
                return {"Error":"Invalid credentials"},401
            access_token = create_access_token(identity=str(user.get("_id")))
            refresh_token = create_refresh_token(identity=str(user.get("_id")))
            user_data = {
                "id":str(user.get("_id")),
                "email":user.get("email"),
                "name":user.get("name"),
                "role":user.get("role"),
                "phone":user.get("phone"),
                "created_at":str(user.get("created_at")),
                "access_token":access_token,
                "refresh_token":refresh_token
            }
            return {"data":user_data}, 200
        except Exception as e:
            print(f"Error in User : {e}")
            return {"Error":"Something wents wrong"},500
        