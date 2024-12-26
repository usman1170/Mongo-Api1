from config import app
from routes import authentication, posts_route


@app.route("/")
def index():
    return {"message":"Welcome to flask app updated"}