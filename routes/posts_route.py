from config import api
from views.posts_view import Create_post, UploadFile, UploadImage, GetAllPosts
 
base_url = "/api/posts"

api.add_resource(Create_post, f"{base_url}/create_post")
api.add_resource(GetAllPosts, f"{base_url}/get-all-posts")
api.add_resource(UploadFile, f"{base_url}/upload-file")
api.add_resource(UploadImage, f"{base_url}/upload-image")