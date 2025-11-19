from datetime import datetime
import tempfile
from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from src.db.posts import Posts
from config import storageManager
from src.utils.posts_utils import validate_image_fields



class Create_post(Resource):
    @jwt_required()
    def post(self):
        
        """ 
        Create Post
        ---
        swagger_from_file: static/swagger/posts/create_post.yml
        """
        try:
            data = request.get_json()
            user_id = get_jwt_identity()
            image = data.get("image")
            if not image:
                return{"message":"Image is missing"},400
            if not validate_image_fields(image) is None:
                response, status_code = validate_image_fields(image)
                return response, status_code

            post_data = {
                "title":data.get("title"),
                "description":data.get("description"),
                "category":data.get("category"),
                "created_at":str(datetime.now()),
                "user_id":ObjectId(user_id),
                "image":image,
            }             
            post = Posts.add_post(post_data)
            if not post:
                return{"message":"post creation failed"},500
            else:
                return{"message":"post created successfully"},201
        except Exception as e:
            print(e)
            return {"Error":"Something wents wrong"},500
        


class GetAllPosts(Resource):
    @jwt_required()
    def get(self):
        """ 
        Get All Posts
        ---
        swagger_from_file: static/swagger/posts/get_all_posts.yml
        """
        try:
            search = request.args.get("search","")
            posts = Posts.get_all_posts(search=search)
            if not posts:
                return{"Posts":[]},200

            return{"Posts":posts},200                
        except Exception as e:
            print(e)
            return {"Error":"Something wents wrong"},500
        

class UploadImage(Resource):
    @jwt_required()
    def post(self):
        """ 
        Upload File
        ---
        swagger_from_file: static/swagger/public/upload_image.yml
        """
        try:
            data = request.files
            image = data.get("image")
            if not image:
                return{"Error":"Image is missing"},404
            temp_dir = tempfile.gettempdir()
            temp_path = f"{temp_dir}/{image.filename}"
            image.save(temp_path)
            new = temp_path.split(".")[-1].lower()
            if new not in ["png","jpg","jpeg"]:
                return{"Error":"Please pick a valid image e.g: .png, .jpg or .jpeg"},400
            resp = storageManager.upload_file_return_url(source_file_name=temp_path, destination_path="usman", randon_name=True)
            if resp["Status"]:
                return{"data":resp},200
            else:
                return{"Error":"Error while uploading image"},500
        except Exception as e:
            print(e)
            return {"Error":f"Something wents wrong: {e}"},500
        


class UploadFile(Resource):
    @jwt_required()
    def post(self):
        """ 
        Upload File
        ---
        swagger_from_file: static/swagger/public/upload_file.yml
        """
        try:
            data = request.files
            image = data.get("image")
            if not image:
                return{"Error":"Image is missing"},404
            temp_dir = tempfile.gettempdir()
            temp_path = f"{temp_dir}/{image.filename}"
            image.save(temp_path)
            resp = storageManager.upload_file_return_url(source_file_name=temp_path, destination_path="usman-files", randon_name=True)
            if resp["Status"]:
                return{"data":resp},200
            else:
                return{"Error":"Error while uploading file"},500
        except Exception as e:
            print(e)
            return {"Error":f"Something wents wrong: {e}"},500
        