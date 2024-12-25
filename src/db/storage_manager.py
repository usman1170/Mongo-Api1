import os
import boto3
from uuid import uuid4

from src.utils.basic import get_file_size


class StorageManager:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"))
        
        self.bucket_name = os.getenv("AWS_BUCKET_NAME")
        
    def create_bucket(self, bucket_name):
        try:
            self.s3.create_bucket(Bucket=bucket_name, ACL="private")
            print("bucket created")
            return {"Status":True}
        except Exception as e:
            return {"Status":False, "message":str(e)}
        
    def check_bucket(self, bucket_name):
        try:
            response = self.s3.head_bucket(Bucket=bucket_name)
            # print(f"Bucket already exists {response}")
            print(f"Bucket already exists....")
        except self.s3.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                resp = self.create_bucket(os.environ.get("AWS_BUCKET_NAME"))
                if resp["Status"]:
                    print(f"bucket created {resp}")
                else:
                    print(f"bucket creation failed: {"message"}")
            
    
    def get_object(self, key):
        try:
            obj = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            return obj
        except Exception as e:
            print(e)
            return False
        
        
    def create_folder(self, name):
        try:
            if not name.endswith("/"):
                name+="/"
            resp = self.s3.put_object(Bucket=self.bucket_name, Key=name)
            return resp
        except Exception as e:
            print(f"Error while folder creating: {e}")
            return False
        
    def download_file(self, filename, filepath):
        try:
            self.s3.download_file(Bucket=self.bucket_name, Key=f"usman/{filename}", Filename=filepath)
            return {"Status":True, "Message":f"File downloaded to {filepath}"}
        except Exception as e:
            print(f"Error while downloading file: {e}")
            return {"Status":False, "Message":f"File downloading failed: {e}"}
        
        
    def upload_file(self, source_file, destination_path, public=True, delete=False):
        try:
            extra_args = {"ACL":"public-read"} if public else {}
            self.s3.upload_file(Filename=source_file, Bucket=self.bucket_name, Key=destination_path)
            if delete:
                os.remove(source_file)
            return True
        except Exception as e:
            print(e)
            return False
        
    def upload_file_return_url(self, source_file_name, destination_path, public=True, delete=False, randon_name=False):
        try:
            data={
                "Status":False,
            }
            if randon_name:
                print("random name generating...")
                uuid_name=str(uuid4()).replace("-","")
                new_name=f"{uuid_name[:5]}{uuid_name[2:8]}{uuid_name[15:22]}{uuid_name[10:18]}{os.path.splitext(source_file_name)[-1]}"
                destination_path = f"{destination_path}/{new_name}"
            data = {
                "size":f"{get_file_size(source_file_name)} kb",
                "original_name":os.path.basename(source_file_name),
                "name":os.path.basename(source_file_name) if not randon_name else new_name,
                "path":destination_path,
            }
            print(data)
            self.upload_file(source_file=source_file_name, destination_path=destination_path, public=public, delete=delete)
            if public:
                
                data["url"] = f"https://s3.{os.getenv("AWS_REGION")}.amazonaws.com/{self.bucket_name}/{destination_path}"
                # data["url"] = f"https://{self.bucket_name}.s3.{os.getenv("AWS_REGION")}.amazonaws.com/{destination_path}"
            data["Status"] = True
            return data
        except Exception as e:
            return None
        

    def generate_presigned_url(self, key, expiration=3600, method="get_object"):
        try:
            url = self.s3.generate_presigned_url(
                ClientMethod=method,
                Params={"Bucket":self.bucket_name, "Key":key},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            print(f"Error generating url = {e}")
            return None
    
        
            