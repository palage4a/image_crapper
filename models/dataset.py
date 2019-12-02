from gridfs import GridFS

class DataSet:
    def __init__(self, db, **kwargs):
        self.db = db
        for name, field in kwargs.items():
            setattr(self, name, field)

    def _put_dataset(self, dataset):
        pass

    def get_dataset(self, dataset):
        pass

    def delete_image_by_url(self, url):
        pass

