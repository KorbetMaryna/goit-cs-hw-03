import argparse
from bson.objectid import ObjectId

from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = f"mongodb://localhost:27017"

client = MongoClient(uri)

db = client.cats_mongo

parser = argparse.ArgumentParser(description="Manage cats database")
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

def create(name, age, features):
    return db.cats.insert_one({
        "name": name, 
        "age": age, 
        "features": features
        })

def read_all():
    """Read all cats from the collection."""
    return list(db.cats.find({}))

def read_by_name(cat_name):
    """Read information about a cat by its name."""
    return db.cats.find_one({"name": cat_name})

def update_age_by_name(cat_name, new_age):
    """ Update the age of a cat by its name. """
    return db.cats.update_one({"name": cat_name}, {"$set": {"age": new_age}})

def add_feature_by_name(cat_name, new_features):
    """Add a new feature to the list of features of a cat by its name."""
    return db.cats.update_one({"name": cat_name}, {"$push": {"features": {"$each": new_features}}})

def delete_by_name(cat_name):
    """Delete a cat by its name."""
    return db.cats.delete_one({"name": cat_name})

def delete_all():
    """Delete all cats from the collection."""
    return db.cats.delete_many({})

if __name__ == "__main__":
    match action:
        case "create":
            response = create(name, age, features)
            print(response.inserted_id)

        case "read":
            if name:
                cat_info = read_by_name(name)
                if cat_info:
                    print(cat_info)
                else:
                    print("Cat not found.")
            else:
                [print(cat) for cat in read_all()]

        case "update":
            if name and age:
                response = update_age_by_name(name, age)
                print(response.modified_count)
            elif name and features:
                response = add_feature_by_name(name, features)
                print(response.modified_count)
            else:
                print("Please provide name along with either age or features to update.")
                
        case "delete":
            if name:
                response = delete_by_name(name)
                print(response.deleted_count)
            else:
                response = delete_all()
                print(response.deleted_count)
        case _:
            print("Wrong action")

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)