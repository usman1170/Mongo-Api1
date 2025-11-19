import os
from flask import jsonify, render_template
from config import app
from routes import authentication, posts_route
from flask_swagger import swagger


@app.route("/")
def index():
    return render_template("index.html")

authorizations = {
    'apiKey': {
        'type': 'apiKey',
        "scheme": "bearer",
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}


@app.route("/swagger")
def api():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "MONGO API"
    swag['securityDefinitions'] = {
        "api_key": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }

    return jsonify(swag)


