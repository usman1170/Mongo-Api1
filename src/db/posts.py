from bson import ObjectId
from config import mongoDBManager
from .pipelines.post_user_pipeline import post_user_pipeline

PostsCol = mongoDBManager.posts
class Posts():
    def __init__(self):
        pass
    
    def add_post(data):
        new_post = PostsCol.insert_one(data)
        return str(new_post.inserted_id)
    

    # def get_all_posts(search="") -> list:
    #     post_list = []
    #     try:
    #         if search:
    #             query = {
    #                 "$or": [
    #                     {"title": {"$regex": search, "$options": "i"}},
    #                     {"category": {"$regex": search, "$options": "i"}}
    #                 ]
    #             }
    #             print(f"Query: {query}")
    #             posts = PostsCol.find(query)
    #         else:
    #             posts = PostsCol.aggregate(post_user_pipeline)

    #         for post in posts:
    #             print(post)
    #             post["_id"] = str(post["_id"])
    #             post["user_id"] = str(post["user_id"])
    #             # post["user"]["_id"] = str(post["user"]["_id"])
    #             if "user" in post:
    #                 post["user"]["_id"] = str(post["user"]["_id"])
    #             else:
    #                 post["user"] = {
    #                     "_id": None,
    #                     "name": "Unknown",
    #                     "email": "Unknown",
    #                     "role": "Unknown",
    #                     "phone": "Unknown"
    #                 }
    #             post_list.append(post)

    #     except Exception as e:
    #         print(f"Error occurred: {e}")
        
    #     return post_list or None


    def get_all_posts(search="") -> list:
        pipeline = post_user_pipeline.copy()
        if search == "":
            posts = PostsCol.aggregate(pipeline)
        else:
            print(f"search is not empty or none: {search}")
            
            match_stage = {
                "$match": {
                    "$or": [
                        {"title": {"$regex": search, "$options": "i"}},
                        {"category": {"$regex": search, "$options": "i"}}
                    ]
                }
            }
            pipeline.insert(0, match_stage)
            posts = PostsCol.aggregate(pipeline)
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
        