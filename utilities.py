from functools import wraps
from flask import (
    Flask, flash, redirect, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

mongo = PyMongo(app)


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
            return redirect(url_for("profile", username=session["username"]))

    return wrap
