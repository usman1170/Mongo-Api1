from config import api
from views.posts_view import Create_post, DownloadFile, GetAllPosts
 
base_url = "/api/posts"

api.add_resource(Create_post, f"{base_url}/create_post")
api.add_resource(GetAllPosts, f"{base_url}/get-all-posts")
api.add_resource(DownloadFile, f"{base_url}/get-file")