import pymongo
class db:
    def __init__(self, option, dbs_read = []):
        self.__db = pymongo.MongoClient("mongodb://localhost:27017/")

    def __getitem__(self, collection):
        return self.__db[collection]