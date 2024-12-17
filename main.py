from config import app
from routes import authentication, posts


@app.route("/")
def index():
    return {"message":"Welcome to flask app"}