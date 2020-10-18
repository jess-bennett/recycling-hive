import os
from datetime import datetime
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/hive")
def get_recycling_categories():
    categories = list(mongo.db.itemCategory.find().sort("categoryName"))
    return render_template(
        "hive.html", categories=categories)


@app.route("/hive/<categoryID>", methods=["GET", "POST"])
def get_recycling_items(categoryID):
    memberID = mongo.db.hiveMembers.find_one(
                {"email": session["user"]})["_id"]
    if request.method == "POST":
        newLocation = {
            "itemID": mongo.db.recyclableItems.find_one(
                {"typeOfWaste": request.form.get("typeOfWaste")})["_id"],
            "conditionNotes": request.form.get("conditionNotes"),
            "charityScheme": request.form.get("charityScheme", None),
            "memberID": memberID,
            "locationID": mongo.db.collectionLocations.find_one(
                {"nickname": request.form.get("locationID"),
                 "memberID": memberID})["_id"],
            "isNational": "no",
            "dateAdded": datetime.now().strftime("%d %b %Y")
        }
        mongo.db.itemCollections.insert_one(newLocation)
        flash("New location added")
        return redirect(url_for("get_recycling_items",
                                categoryID='5f8054dd4361cd9f497a63dd'))
    # Get list of categories for dropdown menu
    categories = list(mongo.db.itemCategory.find().sort("categoryName"))
    # Get recyclable items that match the selected category for
    # # accordion headers
    catItems = list(mongo.db.recyclableItems.find(
        {"categoryID": ObjectId(
            categoryID)}).sort("typeOfWaste"))
    # Create new dictionary of recyclable items and their matching collections
    collectionsDict = mongo.db.itemCollections.aggregate([
        {
         '$lookup': {
            'from': 'recyclableItems',
            'localField': 'itemID',
            'foreignField': '_id',
            'as': 'recyclableItems'
         },
        },
        {'$unwind': '$recyclableItems'},
        {'$project': {
         'recyclableItems': '$recyclableItems.typeOfWaste',
         'id': 1,
         'conditionNotes': 1,
         'charityScheme': 1,
         'typeOfWaste': 1
         }
         },
         {
         '$lookup': {
            'from': 'recyclableItems',
            'localField': 'itemID',
            'foreignField': '_id',
            'as': 'recyclableItems'
         },
        },
        {'$unwind': '$recyclableItems'},
        {'$project': {
         'recyclableItems': '$recyclableItems.typeOfWaste',
         'id': 1,
         'conditionNotes': 1,
         'charityScheme': 1,
         'typeOfWaste': 1
         }
         }
        ])
    # Get list of all recyclable items for dropdown in 'Add location' modal
    items = list(mongo.db.recyclableItems.find().sort("typeOfWaste"))
    # Get list of locations that match the current user's ID for dropdown in
    # 'Add location' modal
    locations = list(mongo.db.collectionLocations.find(
        {"memberID": memberID}).sort("nickname"))
    return render_template(
        "hive-category.html", categoryID=categoryID, categories=categories,
        items=items, locations=locations, catItems=catItems,
        collectionsDict=collectionsDict)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check whether email already exists in db
        existing_user = mongo.db.hiveMembers.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("Email already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username"),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "securityQuestion": request.form.get("security-question"),
            "marketing": request.form.get("marketing")
        }
        mongo.db.hiveMembers.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("email")
        # grab the session user's username from db
        session["username"] = mongo.db.hiveMembers.find_one(
            {"email": session["user"]})["username"]
        flash("Registration Successful!")
        return redirect(url_for("home", username=session["username"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if user exists in db
        existing_user = mongo.db.hiveMembers.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = existing_user["email"]
                # grab the session user's username from db
                session["username"] = mongo.db.hiveMembers.find_one(
                    {"email": session["user"]})["username"]
                return redirect(url_for("home", username=session["username"]))
            else:
                # invalid password match
                flash("Incorrect email and/or password")
                return redirect(url_for("login"))

        else:
            # email doesn't exist
            flash("Incorrect email and/or password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/home/<username>", methods=["GET", "POST"])
def home(username):
    # grab the session user's username from db
    username = mongo.db.hiveMembers.find_one(
        {"email": session["user"]})["username"]

    if session["user"]:
        return render_template("index.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("Log Out Successful!")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
