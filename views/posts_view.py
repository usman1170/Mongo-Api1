
from datetime import datetime
from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from src.db.posts import Posts
from config import storageManager



class Create_post(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            user_id = get_jwt_identity()
            resp = storageManager.upload_file_return_url(source_file_name="D:/Python Flask/Mongo Api1/temp/s3-bnr.jpg", destination_path="usman", randon_name=True)
            
            post_data = {
                "title":data.get("title"),
                "description":data.get("description"),
                "category":data.get("category"),
                "created_at":str(datetime.now()),
                "user_id":ObjectId(user_id),
                "image_url":resp["url"],
                "image_name":resp["original_name"],
                "image_size":resp["size"]
            }
            if resp["Status"]:                
                post = Posts.add_post(post_data)
                if not post:
                    return{"message":"post creation failed"},500
                else:
                    print("post created")
                    return{"message":"post created successfully"},201
            else:
                print("image not uploaded")
                return{"message":"Something wents wrong: Image not uploaded"},400
        except Exception as e:
            print(e)
            return {"Error":"Something wents wrong"},500
        
class GetAllPosts(Resource):
    @jwt_required()
    def get(self):
        try:
            posts = Posts.get_all_posts()
            if not posts:
                return{"message":"post creation failed"},500

            return{"posts":posts},200                
        except Exception as e:
            print(e)
            return {"Error":"Something wents wrong"},500
        

class DownloadFile(Resource):
    # @jwt_required()
    def get(self):
        try:
            # resp = storageManager.download_file(filename="usman.jpg", filepath="D:/Python Flask/Mongo Api1/temp/usman.jpg")
            resp = storageManager.upload_file_return_url(source_file_name="D:/Python Flask/Mongo Api1/temp/s3-bnr.jpg", destination_path="usman", randon_name=True)
            # if not resp["Status"]:
            #     return resp,500
            return{"file":resp},200                
        except Exception as e:
            print(e)
            return {"Error":"Something wents wrong"},500
        