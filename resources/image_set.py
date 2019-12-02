from flask_restful import Resource, reqparse
from utils import Utils

class ImageSetRoute(Resource):
    def __init__(self):
        self.engine_url = "https://bing.com"
        self.query_uri = "/images/async?q=%s&first=%s&count=%s"
    def get(self):
        return {'status': 'get'}
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('dataset', type=str, location="form")
        parser.add_argument('size', type=str,  location="form")
        args = parser.parse_args()
        dataset, size = args['dataset'], args['size']
        url = f'{self.engine_url}{self.query_uri % (dataset,size, size)}'
        souped_page = Utils.get_soup_page(f'{self.engine_url}{self.query_uri % (dataset,size,size)}')
        images = Utils.extract_image_src(souped_page)
        return { "status": "ok" }

    def delete(self):
        return {'status': 'delete'}
