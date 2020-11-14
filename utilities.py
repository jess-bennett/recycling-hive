import os
from datetime import datetime
from functools import wraps
from flask import (
    Flask, flash, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Wraps
def login_required(f):
    '''
    Allow page entry if user logged in
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        if "user" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for("login"))

    return wrap


def approval_required(f):
    '''
    Allow page entry if approved user
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        if mongo.db.hiveMembers.find_one(
                {"_id": ObjectId(session["user_id"]), "approvedMember": True}):
            return f(*args, **kwargs)
        else:
            flash("This page will become viewable once\
                your membership has been approved")
            return redirect(url_for("home"))

    return wrap


def no_demo(f):
    '''
    Allow page entry if not demo user
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        if mongo.db.hiveMembers.find_one(
                {"_id": ObjectId(session["user_id"]),
                 "password": {"$exists": True}}):
            return f(*args, **kwargs)
        else:
            flash("Not available in Demo version")
            return redirect(url_for("home"))

    return wrap


def queen_bee_required(f):
    '''
    Allow page entry if user is Queen Bee
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        if session["member_type"] == "Queen Bee":
            return f(*args, **kwargs)
        else:
            flash("This page is only accessible to Queen Bees")
            return redirect(url_for("home"))

    return wrap


# Functions
def set_session_variables(user, member_type):
    '''
    Set session variables
    '''
    session["user"] = user
    session["username"] = mongo.db.hiveMembers.find_one(
        {"email": session["user"]})["username"]
    session["user_id"] = str(mongo.db.hiveMembers.find_one(
        {"email": session["user"]})["_id"])
    session["hive"] = str(mongo.db.hiveMembers.find_one(
        {"email": session["user"]})["hive"])
    session["member_type"] = member_type
    return


def get_unapproved_members():
    '''
    List members waiting for membership approval
    '''
    unapproved_members = list(mongo.db.hiveMembers.find(
            {"hive": ObjectId(session["hive"]), "approvedMember": False}))
    return unapproved_members


def get_first_collections():
    '''
    List all first collections waiting for approval
    '''
    first_collections = list(mongo.db.firstCollection.find(
        {"hive": ObjectId(session["hive"])}))
    return first_collections


def get_unapproved_collections():
    '''
    List all public collections waiting for approval
    '''
    unapproved_collections = list(mongo.db.publicCollections.find(
        {"hive": ObjectId(session["hive"]), "approvedCollection": False}))
    return unapproved_collections


def create_unnested_list(collection):
    original_list = list(mongo.db[collection].find(
        {}, {"memberID": 1, "_id": 0}))
    unnested_list = list(
        [document["memberID"] for document in original_list])
    return unnested_list


def combine_dictionaries(dict1, dict2):
    '''
    Combine public and private dictionaries into one
    '''
    for item in dict1:
        if item not in dict2:
            dict2.append(item)
            dict2
            dict2
    return dict2


def pop_variables():
    '''
    Remove all session variables
    '''
    session.pop("user")
    session.pop("username")
    session.pop("user_id")
    session.pop("hive")
    session.pop("member_type")
    return


def check_existing_category(value):
    '''
    Check whether field/value already exists
    '''
    mongo.db.itemCategory.find_one(
                {"categoryName_lower": value})
    return


def check_existing_item(value1, value2):
    '''
    Check whether item already exists
    '''
    mongo.db.recyclableItems.find_one(
                {"typeOfWaste_lower": value1,
                 "categoryID": value2})
    return


def get_user_locations(user_id):
    '''
    Get list of users locations
    '''
    locations = list(mongo.db.collectionLocations.find(
        {"memberID": user_id}).sort("nickname"))
    return locations


def get_unapproved_public(user_id):
    '''
    Get list of unapproved public collections
    '''
    unapproved_public_collections = list(mongo.db.publicCollections.find(
            {"memberID": user_id}).sort("businessName"))
    return unapproved_public_collections


def awaiting_approval(user_id):
    '''
    Check whether user has first collection awaiting approval
    '''
    awaiting_approval = mongo.db.firstCollection.find_one(
            {"memberID": user_id})
    if awaiting_approval:
        return True
    else:
        return False


def add_new_category():
    '''
    Add new category and return its ID
    '''
    new_category = {
        "categoryName": request.form.get("newItemCategory"),
        "categoryName_lower": request.form.get(
            "newItemCategory").lower()
    }
    new_category_object = mongo.db.itemCategory.insert_one(new_category)
    category_id = new_category_object.inserted_id
    return category_id


def add_new_item(category_id):
    '''
    Add new item and return its ID
    '''
    new_type_of_waste = {
        "typeOfWaste": request.form.get("newTypeOfWaste"),
        "typeOfWaste_lower": request.form.get(
            "newTypeOfWaste").lower(),
        "categoryID": category_id
    }
    new_type_of_waste_object = mongo.db.recyclableItems.insert_one(
        new_type_of_waste)
    item_id = new_type_of_waste_object.inserted_id
    return item_id


def default_charity_scheme():
    '''
    Check charity scheme and replace with '-' if null
    '''
    charity_scheme = request.form.get("charityScheme")
    if charity_scheme == "":
        charity_scheme = "-"
    return charity_scheme


def new_private_collection(item_id, charityScheme, user_id):
    '''
    Add new collection details to db
    '''
    new_collection = {
        "itemID": item_id,
        "conditionNotes": request.form.get("conditionNotes"),
        "charityScheme": charityScheme,
        "memberID": user_id,
        "locationID": mongo.db.collectionLocations.find_one(
            {"nickname_lower": request.form.get("locationID").lower(),
                "memberID": user_id})["_id"],
        "dateAdded": datetime.now().strftime("%d %b %Y")
    }
    mongo.db.itemCollections.insert_one(new_collection)
    flash("New collection added")
    return


def new_public_collection(collection_type, username,
                          user_id, category_name,
                          type_of_waste, charity_scheme):
    '''
    Add new collection details to db
    '''
    public_collection = {
        "hive": ObjectId(session["hive"]),
        "collectionType": collection_type,
        "username": username,
        "memberID": user_id,
        "categoryName": category_name,
        "typeOfWaste": type_of_waste,
        "conditionNotes": request.form.get("conditionNotes"),
        "charityScheme": charity_scheme,
        "approvedCollection": False,
        "dateAdded": datetime.now().strftime("%d %b %Y")
    }
    public_collection_object = mongo.db.publicCollections.insert_one(
        public_collection)
    public_collection_id = public_collection_object.inserted_id

    filter = {"_id": public_collection_id}
    if collection_type == "local-council":
        new_fields = {"$set": {"councilLocation": request.form.get(
            "councilLocation"), "councilLocation_lower": request.form.get(
                "councilLocation").lower().replace(" ", "_")}}

    if collection_type == "local-other":
        new_fields = {"$set": {"businessName": request.form.get(
            "businessName"), "street": request.form.get(
                "businessStreet"), "town": request.form.get(
                "businessTown"), "postcode": request.form.get(
                "businessPostcode")}}

    if collection_type == "national-postal":
        new_fields = {"$set": {"businessName": request.form.get(
            "businessName"), "street": request.form.get(
                "businessStreet"), "town": request.form.get(
                "businessTown"), "county": request.form.get(
                "businessCounty"), "postcode": request.form.get(
                "businessPostcode")}}

    if collection_type == "national-dropoff":
        new_fields = {"$set": {"businessName": request.form.get(
            "businessName")}}

    mongo.db.publicCollections.update(filter, new_fields)
    flash("Public collection sent for approval")
    return


def create_private_categories_dict():
    '''
    Create dictionary of categories from private collection
    '''
    categories_dict_private = list(mongo.db.itemCollections.aggregate([
            {
             "$lookup": {
                "from": "hiveMembers",
                "localField": "memberID",
                "foreignField": "_id",
                "as": "hiveMembers"
             },
            },
            {"$unwind": "$hiveMembers"},
            {"$match": {"hiveMembers.hive": ObjectId(session["hive"])}},
            {
             "$lookup": {
                "from": "recyclableItems",
                "localField": "itemID",
                "foreignField": "_id",
                "as": "recyclableItems"
             },
            },
            {"$unwind": "$recyclableItems"},
            {
             "$lookup": {
                "from": "itemCategory",
                "localField": "recyclableItems.categoryID",
                "foreignField": "_id",
                "as": "itemCategory"
             },
            },
            {"$unwind": "$itemCategory"},
            {"$group": {
             "_id": "$itemCategory._id",
             "categoryName": {"$first": "$itemCategory.categoryName"}
             }
             },
            {"$sort": {"categoryName": 1}}
            ]))

    return categories_dict_private


def create_public_categories_dict():
    '''
    Create dictionary of categories from public collection
    '''
    categories_dict_public = list(mongo.db.publicCollections.aggregate([
            {"$match": {"approvedCollection": True, "$or": [{"hive": ObjectId(
                session["hive"])}, {"collectionType": "national-postal"},
                {"collectionType": "national-dropoff"}]}},
            {
             "$lookup": {
                "from": "recyclableItems",
                "localField": "itemID",
                "foreignField": "_id",
                "as": "recyclableItems"
             },
            },
            {"$unwind": "$recyclableItems"},
            {
             "$lookup": {
                "from": "itemCategory",
                "localField": "recyclableItems.categoryID",
                "foreignField": "_id",
                "as": "itemCategory"
             },
            },
            {"$unwind": "$itemCategory"},
            {"$group": {
             "_id": "$itemCategory._id",
             "categoryName": {"$first": "$itemCategory.categoryName"}
             }
             },
            {"$sort": {"categoryName": 1}}
            ]))

    return categories_dict_public


def create_private_items_dict():
    '''
    Create dictionary of items from private collection
    '''
    recycling_items_dict_private = list(
            mongo.db.itemCollections.aggregate([
             {
              "$lookup": {
                "from": "hiveMembers",
                "localField": "memberID",
                "foreignField": "_id",
                "as": "hiveMembers"
              },
             },
             {"$unwind": "$hiveMembers"},
             {"$match": {"hiveMembers.hive": ObjectId(session["hive"])}},
             {
              "$lookup": {
                "from": "recyclableItems",
                "localField": "itemID",
                "foreignField": "_id",
                "as": "recyclableItems"
              },
             },
             {"$unwind": "$recyclableItems"},
             {"$group": {
              "_id": "$recyclableItems._id",
              "typeOfWaste": {"$first": "$recyclableItems.typeOfWaste"}
              }
              },
             {"$sort": {"typeOfWaste": 1}}
            ]))

    return recycling_items_dict_private


def create_public_items_dict():
    '''
    Create dictionary of items from public collection
    '''
    recycling_items_dict_public = list(
            mongo.db.publicCollections.aggregate([
                {"$match": {"approvedCollection": True,
                 "$or": [{"hive": ObjectId(
                  session["hive"])}, {"collectionType": "national-postal"},
                  {"collectionType": "national-dropoff"}]}},
                {
                 "$lookup": {
                  "from": "recyclableItems",
                  "localField": "itemID",
                  "foreignField": "_id",
                  "as": "recyclableItems"
                 },
                },
                {"$unwind": "$recyclableItems"},
                {"$group": {
                 "_id": "$recyclableItems._id",
                 "typeOfWaste": {"$first": "$recyclableItems.typeOfWaste"}
                 }
                 },
                {"$sort": {"typeOfWaste": 1}}
            ]))
    return recycling_items_dict_public


def create_private_collector_list():
    '''
    Create list of members with private collections
    '''
    private_collector = list(mongo.db.itemCollections.aggregate([
            {
             "$lookup": {
                "from": "hiveMembers",
                "localField": "memberID",
                "foreignField": "_id",
                "as": "hiveMembers"
             },
            },
            {"$unwind": "$hiveMembers"},
            {"$match": {"hiveMembers.hive": ObjectId(session["hive"])}},
            {"$group": {
             "_id": "$hiveMembers._id",
             "username": {"$first": "$hiveMembers.username"}
             }
             },
            {"$sort": {"username": 1}}
            ]))

    return private_collector


def create_local_council_collector_list():
    '''
    Create list of local council collections
    '''
    local_council_collector = list(
                mongo.db.publicCollections.aggregate([
                    {"$match": {"hive": ObjectId(
                        session["hive"]), "approvedCollection": True,
                        "collectionType": "local-council"}},
                    {"$group": {
                     "_id": "$councilLocation_lower",
                     "councilLocation": {"$first": "$councilLocation"}
                     }
                     },
                    {"$sort": {"_id": 1}}
                    ]))

    return local_council_collector
