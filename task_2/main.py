import argparse
from bson.objectid import ObjectId

from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = f"mongodb://localhost:27017"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client.cats_mongo

parser = argparse.ArgumentParser(description="Add new cat")
parser.add_argument("--action", help="[create, read, update, delete]")
parser.add_argument("--id", help="ID of the cat")
parser.add_argument("--name", help="Name of the cat")
parser.add_argument("--age", help="Age of the cat")
parser.add_argument("--features", help="Features of the cat", nargs='+')

args = vars(parser.parse_args())
action = args["action"]
pk = args["id"]
name = args["name"]
age = args["age"]
features = args["features"]

def read():
    cats = list(db.cats.find({}))
    return cats

def create(name, age, features):
    return db.cats.insert_one({
        "name": name, 
        "age": age, 
        "features": features
        })

def update(pk, name, age, features):
    return db.cats.update_one({"_id": ObjectId(pk)}, {"$set": {"name": name, "age": age, "features": features}})

def delete(pk):
    return db.cats.delete_one({"_id": ObjectId(pk)})

if __name__ == "__main__":
    match action:
        case "create":
            response = create(name, age, features)
            print(response.inserted_id)
        case "read":
            [print(cat) for cat in read()]
        case "update":
            response = update(pk, name, age, features)
            print(response.modified_count)
        case "delete":
            response = delete(pk)
            print(response.deleted_count)
        case _:
            print("Wrong action")

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)