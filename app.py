from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
import gridfs

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_db"
mongo = PyMongo(app)
api = Api(app)

from resources.image_set import ImageSetRoute

api.add_resource(ImageSetRoute, '/')

if __name__ == "__main__":
    app.run(debug=True)
