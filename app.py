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
        "hive-category.html", categories=categories)


@app.route("/hive/items/<categoryID>", methods=["GET", "POST"])
def get_recycling_items(categoryID):
    if categoryID == 'view-all':
        # Get selected category for dropdown
        selectedCategory = 'Select a category'
        # Get recyclable items that match the selected category for
        # # accordion headers
        catItems = list(mongo.db.recyclableItems.find(
        ).sort("typeOfWaste"))
    else:
        # Get selected category for dropdown
        selectedCategory = mongo.db.itemCategory.find_one(
                    {"_id": ObjectId(categoryID)})["categoryName"]
        # Get recyclable items that match the selected category for
        # # accordion headers
        catItems = list(mongo.db.recyclableItems.find(
            {"categoryID": ObjectId(
                categoryID)}).sort("typeOfWaste"))
    # Get list of categories for dropdown menu
    categories = list(mongo.db.itemCategory.find().sort("categoryName"))
    return render_template(
        "hive-item.html",
        categoryID=categoryID, categories=categories, catItems=catItems,
        selectedCategory=selectedCategory)


@app.route("/hive/collections/<itemID>", methods=["GET", "POST"])
def get_recycling_collections(itemID):
    if itemID == 'view-all':
        # Get selected item for dropdown
        selectedItem = 'Select an item'
        # Get recyclable collections that match the selected item for
        # # accordion headers
        itemCollections = list(mongo.db.itemCollections.find(
        ))
    else:
        # Get selected item for dropdown
        selectedItem = mongo.db.recyclableItems.find_one(
                    {"_id": ObjectId(itemID)})["typeOfWaste"]
        # Get recyclable collections that match the selected item for
        # # accordion headers
        itemCollections = list(mongo.db.itemCollections.find(
            {"itemID": ObjectId(
                itemID)}))
    # Get list of items for dropdown menu
    items = list(mongo.db.recyclableItems.find().sort("typeOfWaste"))
    # Create new dictionary of recyclable items and their matching collections
    collectionsDict = list(mongo.db.itemCollections.aggregate([
        {
         '$lookup': {
            'from': 'recyclableItems',
            'localField': 'itemID',
            'foreignField': '_id',
            'as': 'recyclableItems'
         },
        },
        {'$unwind': '$recyclableItems'},
        {
         '$lookup': {
            'from': 'hiveMembers',
            'localField': 'memberID',
            'foreignField': '_id',
            'as': 'hiveMembers'
         },
        },
        {'$unwind': '$hiveMembers'},
        {
         '$lookup': {
            'from': 'collectionLocations',
            'localField': 'locationID',
            'foreignField': '_id',
            'as': 'collectionLocations'
         },
        },
        {'$unwind': '$collectionLocations'},
        {'$project': {
         'typeOfWaste': '$recyclableItems.typeOfWaste',
         'hiveMembers': '$hiveMembers.username',
         'street': '$collectionLocations.street',
         'town': '$collectionLocations.town',
         'postcode': '$collectionLocations.postcode',
         'id': 1,
         'conditionNotes': 1,
         'charityScheme': 1
         }
         }
        ]))
    # Get member ID for adding new location
    memberID = mongo.db.hiveMembers.find_one(
                {"email": session["user"]})["_id"]
    # Get list of all recyclable items for dropdown in 'Add location' modal
    items = list(mongo.db.recyclableItems.find().sort("typeOfWaste"))
    # Get list of locations that match the current user's ID for dropdown in
    # 'Add location' modal
    locations = list(mongo.db.collectionLocations.find(
        {"memberID": memberID}).sort("nickname"))
    # Adding new location
    if request.method == "POST":
        if 'locationID' in request.form:
            itemID = mongo.db.recyclableItems.find_one(
                    {"typeOfWaste": request.form.get("typeOfWaste")})["_id"]
            newCollection = {
                "itemID": mongo.db.recyclableItems.find_one(
                    {"typeOfWaste": request.form.get("typeOfWaste")})["_id"],
                "conditionNotes": request.form.get("conditionNotes"),
                "charityScheme": request.form.get("charityScheme", "-"),
                "memberID": memberID,
                "locationID": mongo.db.collectionLocations.find_one(
                    {"nickname": request.form.get("locationID"),
                     "memberID": memberID})["_id"],
                "isNational": "no",
                "dateAdded": datetime.now().strftime("%d %b %Y")
            }
            mongo.db.itemCollections.insert_one(newCollection)
            flash("New location added")
            return redirect(url_for("get_recycling_collections",
                                    itemID=itemID))
        elif 'addTypeOfWaste' in request.form:
            categoryID = mongo.db.itemCategory.find_one(
                    {"categoryName": request.form.get("itemCategory")})["_id"]
            newItem = {
                "typeOfWaste": request.form.get("addTypeOfWaste"),
                "categoryID": mongo.db.itemCategory.find_one(
                    {"categoryName": request.form.get("itemCategory")})["_id"]
            }
            mongo.db.recyclableItems.insert_one(newItem)
            flash("New Type of Waste added")
            return redirect(url_for("get_recycling_items",
                                    categoryID=categoryID))
        elif 'addCategory' in request.form:
            newCategory = {
                "categoryName": request.form.get("addCategory")
            }
            mongo.db.itemCategory.insert_one(newCategory)
            flash("New Category added")
            return redirect(url_for("get_recycling_categories"))
    # Get list of all item categories for dropdown
    # in 'Add new type of waste' modal
    categories = list(mongo.db.itemCategory.find().sort("categoryName"))
    return render_template(
        "hive-collection.html",
        itemID=itemID, items=items, categories=categories,
        locations=locations, itemCollections=itemCollections,
        collectionsDict=collectionsDict, selectedItem=selectedItem)


@app.route("/hive/members/<memberType>")
def get_recycling_members(memberType):
    if memberType == 'view-all':
        # Get selected member type for dropdown
        selectedMemberType = 'Select a Member Group'
        # Get members that match the selected type for
        # # accordion headers
        memberGroup = list(mongo.db.hiveMembers.find(
        ))
    else:
        # Get selected member type for dropdown
        selectedMemberType = memberType
        # Get members that match the selected type for
        # # accordion headers
        if memberType == 'Queen Bee':
            memberGroup = list(mongo.db.hiveMembers.find(
                {"isQueenBee": True}))
        elif memberType == 'Worker Bee':
            memberGroup = list(mongo.db.hiveMembers.find(
                {"isQueenBee": False, "isWorkerBee": True}))
        elif memberType == 'Busy Bee':
            memberGroup = list(mongo.db.hiveMembers.find(
                {"isQueenBee": False, "isWorkerBee": False}))
    # Create new dictionary of members and their collections
    membersDict = list(mongo.db.itemCollections.aggregate([
        {
         '$lookup': {
            'from': 'recyclableItems',
            'localField': 'itemID',
            'foreignField': '_id',
            'as': 'recyclableItems'
         },
        },
        {'$unwind': '$recyclableItems'},
        {
         '$lookup': {
            'from': 'hiveMembers',
            'localField': 'memberID',
            'foreignField': '_id',
            'as': 'hiveMembers'
         },
        },
        {'$unwind': '$hiveMembers'},
        {
         '$lookup': {
            'from': 'collectionLocations',
            'localField': 'locationID',
            'foreignField': '_id',
            'as': 'collectionLocations'
         },
        },
        {'$unwind': '$collectionLocations'},
        {'$project': {
         'typeOfWaste': '$recyclableItems.typeOfWaste',
         'hiveMembers': '$hiveMembers._id',
         'street': '$collectionLocations.street',
         'town': '$collectionLocations.town',
         'postcode': '$collectionLocations.postcode',
         'id': 1,
         'conditionNotes': 1,
         'charityScheme': 1
         }
         }
        ]))

    return render_template(
        "hive-member.html",
        memberType=memberType, selectedMemberType=selectedMemberType,
        memberGroup=memberGroup, membersDict=membersDict)


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
    # grab the session user's details from db
    userID = mongo.db.hiveMembers.find_one(
        {"email": session["user"]})["_id"]
    email = session["user"]
    if mongo.db.hiveMembers.find_one(
            {"_id": userID, "isQueenBee": True}):
        memberType = "Queen Bee"
    elif mongo.db.hiveMembers.find_one(
            {"_id": userID, "isWorkerBee": True}):
        memberType = "Worker Bee"
    else:
        memberType = "Busy Bee"
    # get user's location details from db
    locations = list(mongo.db.collectionLocations.find(
        {"memberID": userID}).sort("nickname"))
    # Create new dictionary of collections
    collectionsDict = list(mongo.db.itemCollections.aggregate([
        {'$match': {'memberID': userID}},
        {
         '$lookup': {
            'from': 'hiveMembers',
            'localField': 'memberID',
            'foreignField': '_id',
            'as': 'hiveMembers'
         },
        },
        {'$unwind': '$hiveMembers'},
        {
         '$lookup': {
            'from': 'recyclableItems',
            'localField': 'itemID',
            'foreignField': '_id',
            'as': 'recyclableItems'
         },
        },
        {'$unwind': '$recyclableItems'},
        {
         '$lookup': {
            'from': 'collectionLocations',
            'localField': 'locationID',
            'foreignField': '_id',
            'as': 'collectionLocations'
         },
        },
        {'$unwind': '$collectionLocations'},
        {'$project': {
         'typeOfWaste': '$recyclableItems.typeOfWaste',
         'hiveMembers': '$hiveMembers._id',
         'street': '$collectionLocations.street',
         'town': '$collectionLocations.town',
         'postcode': '$collectionLocations.postcode',
         'id': 1,
         'conditionNotes': 1,
         'charityScheme': 1
         }
         }
        ]))
    if session["user"]:
        if request.method == "POST":
            if 'edit-username' in request.form:
                filter = {"_id": ObjectId(userID)}
                session["username"] = request.form.get("edit-username")
                editDetails = { "$set": { 'username': session["username"],
                    "email": request.form.get("edit-email").lower() } }
                print(editDetails)
                mongo.db.hiveMembers.update(filter, editDetails)
                flash("Your details have been updated")
                return redirect(url_for("home", username=session["username"]))
        return render_template("index.html", userID=userID,
                               username=session["username"], email=email,
                               memberType=memberType, locations=locations,
                               collectionsDict=collectionsDict)

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
