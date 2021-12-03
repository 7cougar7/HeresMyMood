import pymongo


def get_user_collection():
    my_client = pymongo.MongoClient(
        "mongodb+srv://APIApplication:application123@cluster0.hurjk.mongodb.net/myFirstDatabase?retryWrites=true&w"
        "=majority"
    )
    my_db = my_client.mydatabase
    return my_db.users


def find_user_doc(uuid=None, email=None):
    user_collect = get_user_collection()
    for user in user_collect.find():
        if user.get('uuid') == uuid or user.get('email') == email:
            return user
    return None
