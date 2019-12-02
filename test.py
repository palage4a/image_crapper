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


class DBTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        from flask_pymongo import PyMongo
        import gridfs
        self.app = app.app
        self.mongo = PyMongo(
                    self.app,
                    uri="mongodb://flask:flask@localhost:27017/test_database?authSource=admin",
                )


    def tearDown(self):
        self.mongo.db.command('dropDatabase')

    @unittest.skip("work")
    def test_db_init(self):
        self.assertEqual(self.mongo.db.name, 'test_database')

    @unittest.skip("work")
    def test_db_create_coll(self):
        self.assertEqual(self.mongo.db.create_collection('test_coll').name, 'test_coll')

    # @unittest.skip("work")
    def test_db_image_put_and_get(self):
        from os import walk
        images = []
        for (_, _, filenames) in walk('for_test'):
            images.extend(filenames)
        dataset = {
                "name": 'cats',
                "length": len(images),
                "images" : []
                }
        img_set = ''
        for image in images:
            with open(f'for_test/{ image }', "rb") as f:
                img_set = f.read()
                dataset[ "images" ].append({
                        "name": image,
                        "binData": img_set
                    })
        post_id = self.mongo.db.datasets.insert_one(dataset).inserted_id
        self.assertEqual(self.mongo.db.datasets.find_one({"_id": post_id})[ "images" ][-1]["binData"], img_set)

@unittest.skip("Not now")
class ModelTestCase(DBTestCase):
    def setUp(self):
        DBTestCase.setUp(self)
        from models.dataset import DataSet
        self.ds_inst = DataSet(self.mongo, name = "test", links = [1,2,3,4])

    def tearDown(self):
        pass
        # self.mongo.db.command('dropDatabase')

    def test__init__(self):
        from models.dataset import DataSet
        self.ds_inst = DataSet(self.mongo, name = "test", links = [1,2,3,4])
        self.assertEqual(self.ds_inst.name, 'test')
        self.assertEqual(type(self.ds_inst), type(DataSet(self.mongo, name="test", links="")))

    @unittest.skip("Not now")
    def test_get_dataset(self):
        pass

    @unittest.skip('Not now')
    def test_put_dataset(self):
        with open('for_test/cats_0', "rb") as f:
            fs_id = self.mongo.put(f.read(), filename = 'test.jpg')
            self.assertEqual(self.fs.get(fs_id).filename, 'test.jpg')

    @unittest.skip("Not now")
    def test_delete_image_by_url(self):
        pass

# @unittest.skip('Not now')
class ImageCrapperTestCase(unittest.TestCase):
    def setUp(self):
        self.host = "http://localhost:5000"
        self.app = app.app.test_client()
        self.maxDiff = None
    def tearDown(self):
        pass

    @unittest.skip('Not now')
    def test_get_req(self):
        result_json = {
                "train" : [ i for i in range( 0, 81 ) ],
                "test" : [ i for i in range( 0, 21 )]
                }
        res = self.app.get(f'{ self.host }/?dataset=cars')
        self.assertEqual(res.status_code, 200)

        self.assertEqual(res.get_json(), {"status": "get"})
        self.assertEqual(
                    len( res.get_json()['train'] ),
                    80
                )

        self.assertEqual(
                    len( res.get_json()['test'] ),
                    20
                )

    # @unittest.skip('Not now')
    def test_post_req(self):

        # TODO: assert prev state set and current ( after posting and getting set)
        res = self.app.post(f'{ self.host }/', data = dict(dataset="cars", size="10"))
        self.assertEqual(res.status_code, 200)
        # self.assertEqual(res.get_json(), {'status': 'ok'})

    @unittest.skip('Not now')
    def test_delete_req(self):

        # TODO: assert prev state set and current ( after delete )

        res = self.app.delete(f'{self.host}/?image=cats.jpg')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {'status': 'ok'})
