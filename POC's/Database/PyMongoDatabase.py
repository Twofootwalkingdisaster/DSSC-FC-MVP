# Importing the mongo client, this library has the complete connection based functions and attributes
from pymongo import MongoClient


# This function is used to connect to the cluster/database we have created at mongodb
def connect_to_atlas():
    # defining the connection address to the database
    # this string is usually available when we create the cluster at mongodb atlas
    database_connection_string = "mongodb://admin:<password>@ac-9wgi5cb-shard-00-00.pwmtrio.mongodb.net:27017,ac-9wgi5cb-shard-00-01.pwmtrio.mongodb.net:27017,ac-9wgi5cb-shard-00-02.pwmtrio.mongodb.net:27017/?ssl=true&replicaSet=atlas-u09bbb-shard-0&authSource=admin&retryWrites=true&w=majority"

    # create a connection with the cluster we created at Mongodb atlas
    mongo_client = MongoClient(database_connection_string)

    # returns the create collection
    return mongo_client['sample_databases']


# This function is used to create and connect to that collection
def connect_to_collections():
    # get the collections that has been created in the database
    database_name = connect_to_atlas()
    print(database_name)
    collection_name = database_name['sample_collection']
    print(collection_name)
    #
    item_1 = {
        "_id": "U1IT00001",
        "item_name": "Blender",
        "max_discount": "10%",
        "batch_number": "RR450020FRG",
        "price": 340,
        "category": "kitchen appliance"
    }

    collection_name.insert_one(item_1)


connect_to_collections()
