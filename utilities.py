import os
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


def check_existing_category(field, value):
    '''
    Check whether category already exists
    '''
    mongo.db.itemCategory.find_one(
                {field: value})
    return
