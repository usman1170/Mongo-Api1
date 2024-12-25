post_user_pipeline=[
            {
                "$lookup":{
                    "from":"users",
                    "localField":"user_id",
                    "foreignField":"_id",
                    "as":"user"
                }
            },
            {
                "$project":{
                    "_id":1,
                    "title":1,
                    "description":1,
                    "category":1,
                    "created_at":1,
                    "user_id":1,
                    "image":1,
                    "user":{
                        "$arrayElemAt":["$user",0]
                    }
                }
            },
            {
                "$project":{
                    "user.password":0,
                    "user.created_at":0,
                }
            },
            {
                "$project":{
                    "image.Status":0,
                    "image.path":0,
                }
            }
        ]