

def validate_image_fields(image_data):
    try:
        required_fields = ["size", "original_name", "name", "path", "url", "Status"]
        for field in required_fields:
            print(field)
            if field not in image_data:
                
                return{"message":f"Missing field in image: {field}"},400
        if not image_data["Status"]:

                return{"message":"Image is not uploaded", "type":{"Status":image_data["Status"]}},400
    except:
        return None
