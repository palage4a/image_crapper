from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

from resources.image_set import ImageSet

api.add_resource(ImageSet, '/')

if __name__ == "__main__":
    app.run(debug=True)
