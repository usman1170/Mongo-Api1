from datetime import timedelta
import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import jwt

from src.db.db_manager import MongoDBManager

load_dotenv()


mongoDBManager = MongoDBManager()
app = Flask(__name__)


app.secret_key = os.environ.get("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)

api = Api(app)
CORS(app)

app.app_context().push()