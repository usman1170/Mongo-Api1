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
                    "image_url":1,
                    "image_name":1,
                    "image_size":1,
                    "user":{
                        "$arrayElemAt":["$user",0]
                    }
                }
            },
            {
                "$project":{
                    "user.password":0
                    # "_id":1,
                    # "title":1,
                    # "description":1,
                    # "category":1,
                    # "created_at":1,
                    # "user_id":1,
                    # "user":{
                    #     "_id":1,
                    #     "name":1,
                    #     "email":1,
                    #     "role":1,
                    #     "phone":1
                    # }
                }
            }
        ]