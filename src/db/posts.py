from bson import ObjectId
from config import mongoDBManager
from .pipelines.post_user import post_user_pipeline

PostsCol = mongoDBManager.posts
class Posts():
    def __init__(self):
        pass
    
    def add_post(data):
        new_post = PostsCol.insert_one(data)
        return str(new_post.inserted_id)
    
    def get_all_posts() -> list:
        posts = PostsCol.aggregate(post_user_pipeline)
        post_list=[]
        if posts:
            for post in posts:
                post["_id"] = str(post["_id"])
                post["user_id"] = str(post["user_id"])
                post["user"]["_id"] = str(post["user"]["_id"])
                post_list.append(post)
            return post_list
        return None
    
    
    def get_post(id=None):
        post = None
        if id:
            post = PostsCol.find_one({"_id":ObjectId(id)})
        if post:
            post["_id"] = str(post["_id"])
            return post
        return None
        