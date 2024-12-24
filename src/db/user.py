from bson import ObjectId
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
        user = UserCol.insert_one(data.dict())
        return str(user.inserted_id)
        
        
        
    
    @staticmethod
    def get_user(email=None, id=None):
        user = None
        if email:
            user = UserCol.find_one({"email":email})
        if id:
            user = UserCol.find_one({"_id":ObjectId(id)})
        if user:
            user["_id"] = str(user["_id"])
            user["created_at"] = str(user["created_at"])
            return user
        return None
        