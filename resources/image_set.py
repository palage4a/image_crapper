from flask_restful import Resource, reqparse
from utils import Utils

class ImageSet(Resource):
    def __init__(self):
        self.engine_url = "https://bing.com"
        self.query_uri = "/images/async?q=%s&first=%s&count=%s"
    def get(self):
        return {'status': 'get'}
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('dataset', type=str, location="args")
        parser.add_argument('size', type=int,  location="args")
        args = parser.parse_args()
        dataset, size = args['dataset'], args['size']
        souped_page = Utils.get_soup_page(f'{self.engine_url}{self.query_uri % (dataset,size, size)}')
        return { "status":  repr(result[:size])}

    def delete(self):
        return {'status': 'delete'}
