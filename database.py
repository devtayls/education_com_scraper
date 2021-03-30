from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
database = client['education_com_resources']


def insert_item(dict, collection='worksheets'):
    # created field on the document
    dict['created'] = datetime.today()

    x = database[collection].insert_one(dict)
    print(x)


def query(collection, query=''):
    # TODO is this behavior correct? will it fail for having an empty string?
    if query:
        database[collection].find(query)
    else:
        database[collection].find(query)
