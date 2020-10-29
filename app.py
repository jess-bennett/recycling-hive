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
def home():
    try:
        users = mongo.db.hiveMembers

        return render_template("pages/index.html",
                               username=users.find_one(
                                   {'email': session['user']})["username"],
                               pageID="home")
    except:
        return render_template(
            "pages/index.html", username=False, pageID="home")


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
            "marketing": request.form.get("marketing"),
            "isQueenBee": False,
            "isWorkerBee": False
        }
        mongo.db.hiveMembers.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("email")
        # grab the session user's username from db
        session["username"] = mongo.db.hiveMembers.find_one(
            {"email": session["user"]})["username"]
        flash("Registration Successful!")
        return redirect(url_for("home", username=session["username"]))

    return render_template("pages/register.html", pageID="register")


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
                return redirect(url_for("home"))
            else:
                # invalid password match
                flash("Incorrect email and/or password")
                return redirect(url_for("login"))

        else:
            # email doesn't exist
            flash("Incorrect email and/or password")
            return redirect(url_for("login"))

    return render_template("pages/login.html", pageID="login")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if session["user"]:
        # grab the session user's details from db
        userID = mongo.db.hiveMembers.find_one(
            {'email': session['user']})["_id"]
        email = session["user"]
        if mongo.db.hiveMembers.find_one(
                {"_id": userID, "isQueenBee": True}):
            memberType = "Queen Bee"
        elif mongo.db.hiveMembers.find_one(
                {"_id": userID, "isWorkerBee": True}):
            memberType = "Worker Bee"
        else:
            memberType = "Busy Bee"
        # get user's location details from db for location accordion
        locations = list(mongo.db.collectionLocations.find(
            {"memberID": userID}).sort("nickname"))
        # Create new dictionary of collections for collection accordion
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
        # Get list of categories for dropdown menu
        categories = list(mongo.db.itemCategory.find().sort("categoryName"))
        # Get list of all recyclable items for
        # dropdown in 'Add collection' modal
        items = list(mongo.db.recyclableItems.find().sort("typeOfWaste"))
        itemsDict = list(mongo.db.recyclableItems.aggregate([
            {
             '$lookup': {
                'from': 'itemCategory',
                'localField': 'categoryID',
                'foreignField': '_id',
                'as': 'itemCategory'
             },
            },
            {'$unwind': '$itemCategory'}
            ]))
        # Post method for editing user details
        if request.method == "POST":
            # check where email already exists in db
            existing_user = mongo.db.hiveMembers.find_one(
                {"_id": {"$ne": ObjectId(userID)},
                    "email": request.form.get("edit-email").lower()}
            )
            if existing_user:
                flash("Email already exists")
                return redirect(url_for(
                    "profile", username=session["username"]))

            filter = {"_id": ObjectId(userID)}
            session["username"] = request.form.get("edit-username")
            editDetails = {"$set": {'username': session["username"],
                           "email": request.form.get(
                            "edit-email").lower()}}
            mongo.db.hiveMembers.update(filter, editDetails)
            flash("Your details have been updated")
            return redirect(url_for(
                "profile", username=session["username"]))

        return render_template("/pages/profile.html", userID=userID,
                               username=session["username"], email=email,
                               memberType=memberType, locations=locations,
                               collectionsDict=collectionsDict, items=items,
                               itemsDict=itemsDict, categories=categories,
                               pageID="profile")

    return redirect(url_for("login"))


@app.route("/profile/delete")
def deleteProfile():
    # grab the session user's details from db
    userID = mongo.db.hiveMembers.find_one(
            {'email': session['user']})["_id"]
    mongo.db.hiveMembers.remove({"_id": ObjectId(userID)})
    mongo.db.collectionLocations.remove({"memberID": ObjectId(userID)})
    mongo.db.itemCollections.remove({"memberID": ObjectId(userID)})
    flash("Your profile has been successfully deleted")
    return redirect(url_for("logout"))


@app.route("/add-new-location", methods=["GET", "POST"])
def add_new_location():
    userID = mongo.db.hiveMembers.find_one({'email': session['user']})["_id"]
    if request.method == "POST":
        # Check whether nickname already exists
        existingNickname = mongo.db.collectionLocations.find_one(
            {"memberID": ObjectId(userID), "nickname": request.form.get(
                "addLocationNickname")})
        if existingNickname:
            flash("Location already saved under this nickname")
            return redirect(url_for("profile", username=session["username"]))
        newLocation = {
                "nickname": request.form.get("addLocationNickname"),
                "street": request.form.get("addLocationStreet"),
                "town": request.form.get("addLocationTown"),
                "postcode": request.form.get("addLocationPostcode"),
                "memberID": userID
            }
        mongo.db.collectionLocations.insert_one(newLocation)
        flash("New location added")
        return redirect(url_for("profile", username=session["username"]))

    return redirect(url_for("profile", username=session["username"]))


@app.route("/delete-location/<locationID>")
def deleteLocation(locationID):
    mongo.db.collectionLocations.remove({"_id": ObjectId(locationID)})
    mongo.db.itemCollections.remove({"locationID": ObjectId(locationID)})
    flash("Your location has been successfully deleted")
    return redirect(url_for("profile", username=session["username"]))


@app.route("/add-new-item", methods=["GET", "POST"])
def add_new_item():
    userID = mongo.db.hiveMembers.find_one(
            {'email': session['user']})["_id"]
    if request.method == "POST":
        # Post method for adding a new category and type of waste
        if 'newItemCategory' in request.form:
            # Check whether category already exists
            existingCategory = mongo.db.itemCategory.find_one(
                {"categoryName": request.form.get(
                    "newItemCategory")})

            if existingCategory:
                flash("Category already exists")
                return redirect(url_for(
                    "profile", username=session["username"]))

            newItemCategory = {
                "categoryName": request.form.get("newItemCategory")
            }
            mongo.db.itemCategory.insert_one(newItemCategory)
            categoryID = mongo.db.itemCategory.find_one(
                    {"categoryName": request.form.get(
                        "newItemCategory")})["_id"]

            # Check whether item already exists
            existingTypeOfWaste = mongo.db.recyclableItems.find_one(
                {"typeOfWaste": request.form.get("newTypeOfWaste"),
                    "categoryID": categoryID}
            )
            if existingTypeOfWaste:
                flash("Type of Waste already exists for this category")
                return redirect(url_for(
                    "profile", username=session["username"]))

            newTypeOfWaste = {
                "typeOfWaste": request.form.get("newTypeOfWaste"),
                "categoryID": categoryID
            }
            mongo.db.recyclableItems.insert_one(newTypeOfWaste)
            itemID = mongo.db.recyclableItems.find_one(
                    {"typeOfWaste": request.form.get(
                        "newTypeOfWaste")})["_id"]
            newCollection = {
                "itemID": itemID,
                "conditionNotes": request.form.get("conditionNotes"),
                "charityScheme": request.form.get("charityScheme"),
                "memberID": userID,
                "locationID": mongo.db.collectionLocations.find_one(
                    {"nickname": request.form.get("locationID"),
                        "memberID": userID})["_id"],
                "isNational": "no",
                "dateAdded": datetime.now().strftime("%d %b %Y")
            }
            mongo.db.itemCollections.insert_one(newCollection)
            flash("New collection added")
            return redirect(url_for("get_recycling_collections",
                                    itemID=itemID))
        # Post method for adding new type of waste with existing category
        if 'newTypeOfWaste' in request.form:
            # Check whether item already exists
            existingTypeOfWaste = mongo.db.recyclableItems.find_one(
                {"typeOfWaste": request.form.get("newTypeOfWaste"),
                    "categoryID": mongo.db.itemCategory.find_one(
                    {"categoryName": request.form.get(
                        "itemCategory")})["_id"]}
            )
            if existingTypeOfWaste:
                flash("Type of Waste already exists for this category")
                return redirect(url_for(
                    "profile", username=session["username"]))

            newTypeOfWaste = {
                "typeOfWaste": request.form.get("newTypeOfWaste"),
                "categoryID": mongo.db.itemCategory.find_one(
                    {"categoryName": request.form.get(
                        "itemCategory")})["_id"]
            }
            mongo.db.recyclableItems.insert_one(newTypeOfWaste)
            itemID = mongo.db.recyclableItems.find_one(
                    {"typeOfWaste": request.form.get(
                        "newTypeOfWaste")})["_id"]
            newCollection = {
                "itemID": itemID,
                "conditionNotes": request.form.get("conditionNotes"),
                "charityScheme": request.form.get("charityScheme"),
                "memberID": userID,
                "locationID": mongo.db.collectionLocations.find_one(
                    {"nickname": request.form.get("locationID"),
                        "memberID": userID})["_id"],
                "isNational": "no",
                "dateAdded": datetime.now().strftime("%d %b %Y")
            }
            mongo.db.itemCollections.insert_one(newCollection)
            flash("New collection added")
            return redirect(url_for("get_recycling_collections",
                                    itemID=itemID))
        # Post method for adding new collection with existing type
        # of waste and category
        if 'typeOfWaste' in request.form:
            itemID = mongo.db.recyclableItems.find_one(
                    {"typeOfWaste": request.form.get(
                        "typeOfWaste")})["_id"]
            newCollection = {
                "itemID": itemID,
                "conditionNotes": request.form.get("conditionNotes"),
                "charityScheme": request.form.get("charityScheme"),
                "memberID": userID,
                "locationID": mongo.db.collectionLocations.find_one(
                    {"nickname": request.form.get("locationID"),
                        "memberID": userID})["_id"],
                "isNational": "no",
                "dateAdded": datetime.now().strftime("%d %b %Y")
            }
            mongo.db.itemCollections.insert_one(newCollection)
            flash("New collection added")
            return redirect(url_for("get_recycling_collections",
                                    itemID=itemID))
    return redirect(url_for("profile", username=session["username"]))


@app.route("/hive")
def get_recycling_categories():
    categories = list(mongo.db.itemCategory.find().sort("categoryName"))
    return render_template(
        "pages/hive-category.html", categories=categories, pageID="categories")


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
        "pages/hive-item.html",
        categoryID=categoryID, categories=categories, catItems=catItems,
        selectedCategory=selectedCategory, pageID="items")


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

    return render_template(
        "pages/hive-collection.html",
        itemID=itemID, items=items, itemCollections=itemCollections,
        collectionsDict=collectionsDict, selectedItem=selectedItem,
        pageID="collections")


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
    # Check if member has collection
    membersCollection = list(mongo.db.itemCollections.find(
        {}, {"memberID": 1, "_id": 0}))
    membersCollectionValues = list(
        [document["memberID"] for document in membersCollection])
    # Create new dictionary of members and their collections
    membersDict = list(mongo.db.hiveMembers.aggregate([
        {
         '$lookup': {
            'from': 'itemCollections',
            'localField': '_id',
            'foreignField': 'memberID',
            'as': 'itemCollections'
         },
        },
        {'$unwind': '$itemCollections'},
        {
         '$lookup': {
            'from': 'recyclableItems',
            'localField': 'itemCollections.itemID',
            'foreignField': '_id',
            'as': 'recyclableItems'
         },
        },
        {'$unwind': '$recyclableItems'},
        {
         '$lookup': {
            'from': 'collectionLocations',
            'localField': 'itemCollections.locationID',
            'foreignField': '_id',
            'as': 'collectionLocations'
         },
        },
        {'$unwind': '$collectionLocations'},
        {'$project': {
         'typeOfWaste': '$recyclableItems.typeOfWaste',
         'street': '$collectionLocations.street',
         'town': '$collectionLocations.town',
         'postcode': '$collectionLocations.postcode',
         'conditionNotes': '$itemCollections.conditionNotes',
         'charityScheme': '$itemCollections.charityScheme'
         }
         },
        {'$sort': {'typeOfWaste': 1}}
        ]))
    return render_template(
        "pages/hive-member.html",
        memberType=memberType, selectedMemberType=selectedMemberType,
        memberGroup=memberGroup, membersDict=membersDict,
        membersCollection=membersCollection,
        membersCollectionValues=membersCollectionValues, pageID="members")


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("Log Out Successful!")
    session.pop("user")
    session.pop("username")
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
