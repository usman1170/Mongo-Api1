
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
            image = data.get("image")
            if not image:
                return{"message":"Image is missing"},400

            resp = storageManager.upload_file_return_url(source_file_name=image, destination_path="usman", randon_name=True)
            post_data = {
                "title":data.get("title"),
                "description":data.get("description"),
                "category":data.get("category"),
                "created_at":str(datetime.now()),
                "user_id":ObjectId(user_id),
                "image":resp,
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
            search = request.args.get("search","")
            posts = Posts.get_all_posts(search=search)
            if not posts:
                return{"Posts":[]},200

            return{"Posts":posts},200                
        except Exception as e:
            print(e)
            return {"Error":"Something wents wrong"},500
        

class DownloadFile(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            image = data.get("image")
            if not image:
                return{"Error":"Image is missing"},404
            url = storageManager.generate_presigned_url(key=image)
            if url:
                return{"url":url},200
            else:
                return{"Error":"Error while generating url"},500
        except Exception as e:
            print(e)
            return {"Error":"Something wents wrong"},500
        