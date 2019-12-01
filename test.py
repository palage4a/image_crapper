import unittest
import json
import requests
import bs4

import app
from utils import Utils

@unittest.skip("Working")
class UtilsTestCase(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.imageSet_inst = app.ImageSetRoute()
        self.engine_url = self.imageSet_inst.engine_url
        self.dataset = 'cats'
        self.header = {
                'User-Agent' :
                    'Mozilla/5.0 (X11; Linux x86_64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/78.0.3904.108 Safari/537.36'
            }
        self.query_uri = self.imageSet_inst.query_uri % (self.dataset, 10, 10)
        self.query_uri_100 = self.imageSet_inst.query_uri % (self.dataset, 100, 100)
    def tearDown(self):
        pass

    def test_get_soup_page(self):
        test_query = f"{self.engine_url}{self.query_uri}"
        # Check count of container with images
        self.assertEqual(
                    1,
                    len(Utils.get_soup_page(test_query).find_all(id="mmComponent_images_1"))
                )
        # Check count of li-tags with images
        self.assertEqual(
                    10,
                    len( Utils.get_soup_page(test_query).find(id="mmComponent_images_1").find_all('li'))
                )

    def test_get_soup_page_100(self):
        test_query = f"{self.engine_url}{self.query_uri_100}"
        # Check count of container with images
        self.assertEqual(
                    1,
                    len(Utils.get_soup_page(test_query).find_all(id="mmComponent_images_1"))
                )
        # Check count of li-tags with images
        self.assertEqual(
                    100,
                    len( Utils.get_soup_page(test_query).find(id="mmComponent_images_1").find_all('li'))
                )

    def test_extract_image_src(self):
        test_query = f"{self.engine_url}{self.query_uri}"
        res = requests.get(test_query, headers = self.header)
        res_soup = bs4.BeautifulSoup(res.text, 'html.parser')
        self.assertEqual(
               10,
               len(Utils.extract_image_src(res_soup))
               )

    def test_extract_image_src_100(self):
        test_query = f"{self.engine_url}{self.query_uri_100}"
        res = requests.get(test_query, headers = self.header)
        res_soup = bs4.BeautifulSoup(res.text, 'html.parser')
        self.assertEqual(
               100,
               len(Utils.extract_image_src(res_soup))
               )


    def test_download_image(self):
        test_query = f"{self.engine_url}{self.query_uri}"
        page = Utils.get_soup_page(test_query)
        img_srcs = Utils.extract_image_src(page)
        self.assertEqual(
                    10,
                    Utils.download_images(img_srcs, self.dataset)
                )

    def test_download_image_100(self):
        test_query = f"{self.engine_url}{self.query_uri_100}"
        page = Utils.get_soup_page(test_query)
        img_srcs = Utils.extract_image_src(page)
        self.assertEqual(
                    100,
                    Utils.download_images(img_srcs, self.dataset)
                )


@unittest.skip('no')
class DBTestCase(unittest.TestCase):

    def setUp(self):
        from flask_pymongo import PyMongo
        import gridfs
        self.app= app.app
        self.mongo= PyMongo(
                    self.app,
                    uri="mongodb://flask:flask@localhost:27017/test_database?authSource=admin",
                )

        self.fs_db= PyMongo(
                    self.app,
                    uri="mongodb://flask:flask@localhost:27017/test_gridfs?authSource=admin",
                )
        self.fs= gridfs.GridFS(self.fs_db.db)

    def tearDown(self):
        self.mongo.db.command('dropDatabase')

    def test_db_init(self):
        self.assertEqual(self.mongo.db.name, 'test_database')
        self.assertEqual(self.fs_db.db.name, 'test_gridfs')

    def test_db_create_coll(self):
        self.assertEqual(self.mongo.db.create_collection('test_coll').name, 'test_coll')

    def test_db_fs_init(self):
        self.assertEqual(self.fs_db.db.name, 'test_gridfs')

    def test_db_fs_put_and_get(self):
        test_input = self.fs.put(b"test")
        self.assertEqual(self.fs.get(test_input).read(), b"test")

@unittest.skip('')
class ImageCrapperTestCase(unittest.TestCase):
    def setUp(self):
        self.host = "http://localhost:5000"
        self.app = app.app.test_client()
        self.maxDiff = None
    def tearDown(self):
        pass

    @unittest.skip('because')
    def test_get_req(self):
        result_json = {
                "train" : [],
                "test" : []
                }
        res = self.app.get(f'{ self.host }/?dataset=cats')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {'status': 'get'})

    @unittest.skip("because")
    def test_post_req(self):
        res = self.app.post(f'{ self.host }/?dataset=cats&size=10')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {'status': 'post'})

    @unittest.skip('because')
    def test_delete_req(self):
        res = self.app.delete(f'{self.host}/?image=cats.jpg')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {'status': 'delete'})
