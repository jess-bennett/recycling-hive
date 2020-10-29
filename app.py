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
                               page_id="home")
    except:
        return render_template(
            "pages/index.html", username=False, page_id="home")


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
            "securityQuestion": request.form.get("securityQuestion"),
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

    return render_template("pages/register.html", page_id="register")


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

    return render_template("pages/login.html", page_id="login")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if session["user"]:
        # grab the session user's details from db
        user_id = mongo.db.hiveMembers.find_one(
            {'email': session['user']})["_id"]
        email = session["user"]
        if mongo.db.hiveMembers.find_one(
                {"_id": user_id, "isQueenBee": True}):
            member_type = "Queen Bee"
        elif mongo.db.hiveMembers.find_one(
                {"_id": user_id, "isWorkerBee": True}):
            member_type = "Worker Bee"
        else:
            member_type = "Busy Bee"
        # get user's location details from db for location accordion
        locations = list(mongo.db.collectionLocations.find(
            {"memberID": user_id}).sort("nickname"))
        # Create new dictionary of collections for collection accordion
        collections_dict = list(mongo.db.itemCollections.aggregate([
            {'$match': {'memberID': user_id}},
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
             'nickname': '$collectionLocations.nickname',
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
        items_dict = list(mongo.db.recyclableItems.aggregate([
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
                {"_id": {"$ne": ObjectId(user_id)},
                    "email": request.form.get("edit-email").lower()}
            )
            if existing_user:
                flash("Email already exists")
                return redirect(url_for(
                    "profile", username=session["username"]))

            filter = {"_id": ObjectId(user_id)}
            session["username"] = request.form.get("edit-username")
            edit_details = {"$set": {'username': session["username"],
                            "email": request.form.get(
                            "edit-email").lower()}}
            mongo.db.hiveMembers.update(filter, edit_details)
            flash("Your details have been updated")
            return redirect(url_for(
                "profile", username=session["username"]))

        return render_template("/pages/profile.html", user_id=user_id,
                               username=session["username"], email=email,
                               member_type=member_type, locations=locations,
                               collections_dict=collections_dict, items=items,
                               items_dict=items_dict, categories=categories,
                               page_id="profile")

    return redirect(url_for("login"))


@app.route("/profile/delete")
def delete_profile():
    # grab the session user's details from db
    user_id = mongo.db.hiveMembers.find_one(
            {'email': session['user']})["_id"]
    mongo.db.hiveMembers.remove({"_id": ObjectId(user_id)})
    mongo.db.collectionLocations.remove({"memberID": ObjectId(user_id)})
    mongo.db.itemCollections.remove({"memberID": ObjectId(user_id)})
    flash("Your profile has been successfully deleted")
    return redirect(url_for("logout"))


@app.route("/add-new-location", methods=["GET", "POST"])
def add_new_location():
    user_id = mongo.db.hiveMembers.find_one({'email': session['user']})["_id"]
    if request.method == "POST":
        # Check whether nickname already exists
        existing_nickname = mongo.db.collectionLocations.find_one(
            {"memberID": ObjectId(user_id), "nickname": request.form.get(
                "addLocationNickname")})
        if existing_nickname:
            flash("Location already saved under this nickname")
            return redirect(url_for("profile", username=session["username"]))
        new_location = {
                "nickname": request.form.get("addLocationNickname"),
                "street": request.form.get("addLocationStreet"),
                "town": request.form.get("addLocationTown"),
                "postcode": request.form.get("addLocationPostcode"),
                "memberID": user_id
            }
        mongo.db.collectionLocations.insert_one(new_location)
        flash("New location added")
        return redirect(url_for("profile", username=session["username"]))

    return redirect(url_for("profile", username=session["username"]))


@app.route("/edit-location/<location_id>", methods=["GET", "POST"])
def edit_location(location_id):
    if request.method == "POST":
        filter = {"_id": ObjectId(location_id)}
        edit_location = {"$set": {"street": request.form.get("editStreet"),
                        "town": request.form.get("editTown"),
                        "postcode": request.form.get("editPostcode")}}
        mongo.db.collectionLocations.update(filter, edit_location)
        flash("Your location has been updated")
        return redirect(url_for(
            "profile", username=session["username"]))

    return redirect(url_for("profile", username=session["username"]))


@app.route("/delete-location/<location_id>")
def delete_location(location_id):
    mongo.db.collectionLocations.remove({"_id": ObjectId(location_id)})
    mongo.db.itemCollections.remove({"locationID": ObjectId(location_id)})
    flash("Your location has been successfully deleted")
    return redirect(url_for("profile", username=session["username"]))


@app.route("/add-new-collection", methods=["GET", "POST"])
def add_new_collection():
    user_id = mongo.db.hiveMembers.find_one(
            {'email': session['user']})["_id"]
    if request.method == "POST":
        # Post method for adding a new category and type of waste
        if 'newItemCategory' in request.form:
            # Check whether category already exists
            existing_category = mongo.db.itemCategory.find_one(
                {"categoryName": request.form.get(
                    "newItemCategory")})

            if existing_category:
                flash("Category already exists")
                return redirect(url_for(
                    "profile", username=session["username"]))

            new_item_category = {
                "categoryName": request.form.get("newItemCategory")
            }
            mongo.db.itemCategory.insert_one(new_item_category)
            category_id = mongo.db.itemCategory.find_one(
                    {"categoryName": request.form.get(
                        "newItemCategory")})["_id"]

            # Check whether item already exists
            existing_type_of_waste = mongo.db.recyclableItems.find_one(
                {"typeOfWaste": request.form.get("newTypeOfWaste"),
                    "categoryID": category_id}
            )
            if existing_type_of_waste:
                flash("Type of Waste already exists for this category")
                return redirect(url_for(
                    "profile", username=session["username"]))

            new_type_of_waste = {
                "typeOfWaste": request.form.get("newTypeOfWaste"),
                "categoryID": category_id
            }
            mongo.db.recyclableItems.insert_one(new_type_of_waste)
            item_id = mongo.db.recyclableItems.find_one(
                    {"typeOfWaste": request.form.get(
                        "newTypeOfWaste")})["_id"]
            new_collection = {
                "itemID": item_id,
                "conditionNotes": request.form.get("conditionNotes"),
                "charityScheme": request.form.get("charityScheme"),
                "memberID": user_id,
                "locationID": mongo.db.collectionLocations.find_one(
                    {"nickname": request.form.get("locationID"),
                        "memberID": user_id})["_id"],
                "isNational": "no",
                "dateAdded": datetime.now().strftime("%d %b %Y")
            }
            mongo.db.itemCollections.insert_one(new_collection)
            flash("New collection added")
            return redirect(url_for("get_recycling_collections",
                                    item_id=item_id))
        # Post method for adding new type of waste with existing category
        if 'newTypeOfWaste' in request.form:
            # Check whether item already exists
            existing_type_of_waste = mongo.db.recyclableItems.find_one(
                {"typeOfWaste": request.form.get("newTypeOfWaste"),
                    "categoryID": mongo.db.itemCategory.find_one(
                    {"categoryName": request.form.get(
                        "itemCategory")})["_id"]}
            )
            if existing_type_of_waste:
                flash("Type of Waste already exists for this category")
                return redirect(url_for(
                    "profile", username=session["username"]))

            new_type_of_waste = {
                "typeOfWaste": request.form.get("newTypeOfWaste"),
                "categoryID": mongo.db.itemCategory.find_one(
                    {"categoryName": request.form.get(
                        "itemCategory")})["_id"]
            }
            mongo.db.recyclableItems.insert_one(new_type_of_waste)
            item_id = mongo.db.recyclableItems.find_one(
                    {"typeOfWaste": request.form.get(
                        "newTypeOfWaste")})["_id"]
            new_collection = {
                "itemID": item_id,
                "conditionNotes": request.form.get("conditionNotes"),
                "charityScheme": request.form.get("charityScheme"),
                "memberID": user_id,
                "locationID": mongo.db.collectionLocations.find_one(
                    {"nickname": request.form.get("locationID"),
                        "memberID": user_id})["_id"],
                "isNational": "no",
                "dateAdded": datetime.now().strftime("%d %b %Y")
            }
            mongo.db.itemCollections.insert_one(new_collection)
            flash("New collection added")
            return redirect(url_for("get_recycling_collections",
                                    item_id=item_id))
        # Post method for adding new collection with existing type
        # of waste and category
        if 'typeOfWaste' in request.form:
            item_id = mongo.db.recyclableItems.find_one(
                    {"typeOfWaste": request.form.get(
                        "typeOfWaste")})["_id"]
            new_collection = {
                "itemID": item_id,
                "conditionNotes": request.form.get("conditionNotes"),
                "charityScheme": request.form.get("charityScheme"),
                "memberID": user_id,
                "locationID": mongo.db.collectionLocations.find_one(
                    {"nickname": request.form.get("locationID"),
                        "memberID": user_id})["_id"],
                "isNational": "no",
                "dateAdded": datetime.now().strftime("%d %b %Y")
            }
            mongo.db.itemCollections.insert_one(new_collection)
            flash("New collection added")
            return redirect(url_for("get_recycling_collections",
                                    item_id=item_id))
    return redirect(url_for("profile", username=session["username"]))


@app.route("/edit-collection/<collection_id>", methods=["GET", "POST"])
def edit_collection(collection_id):
    if request.method == "POST":
        filter = {"_id": ObjectId(collection_id)}
        edit_collection = {"$set":
                           {"conditionNotes": request.form.get("editNotes"),
                            "charityScheme": request.form.get("editCharity"),
                            "locationID": ObjectId(
                                request.form.get("editLocation"))}}
        mongo.db.itemCollections.update(filter, edit_collection)
        flash("Your collection has been updated")
        return redirect(url_for(
            "profile", username=session["username"]))

    return redirect(url_for("profile", username=session["username"]))


@app.route("/delete-collection/<collection_id>")
def delete_collection(collection_id):
    mongo.db.itemCollections.remove({"_id": ObjectId(collection_id)})
    flash("Your collection has been successfully deleted")
    return redirect(url_for("profile", username=session["username"]))


@app.route("/hive")
def get_recycling_categories():
    categories = list(mongo.db.itemCategory.find().sort("categoryName"))
    return render_template(
        "pages/hive-category.html",
        categories=categories, page_id="categories")


@app.route("/hive/items/<category_id>", methods=["GET", "POST"])
def get_recycling_items(category_id):
    if category_id == 'view-all':
        # Get selected category for dropdown
        selected_category = 'Select a category'
        # Get recyclable items that match the selected category for
        # # accordion headers
        cat_items = list(mongo.db.recyclableItems.find(
        ).sort("typeOfWaste"))
    else:
        # Get selected category for dropdown
        selected_category = mongo.db.itemCategory.find_one(
                    {"_id": ObjectId(category_id)})["categoryName"]
        # Get recyclable items that match the selected category for
        # # accordion headers
        cat_items = list(mongo.db.recyclableItems.find(
            {"categoryID": ObjectId(
                category_id)}).sort("typeOfWaste"))
    # Get list of categories for dropdown menu
    categories = list(mongo.db.itemCategory.find().sort("categoryName"))
    return render_template(
        "pages/hive-item.html",
        category_id=category_id, categories=categories, cat_items=cat_items,
        selected_category=selected_category, page_id="items")


@app.route("/hive/collections/<item_id>", methods=["GET", "POST"])
def get_recycling_collections(item_id):
    if item_id == 'view-all':
        # Get selected item for dropdown
        selected_item = 'Select an item'
        # Get recyclable collections that match the selected item for
        # # accordion headers
        item_collections = list(mongo.db.itemCollections.find(
        ))
    else:
        # Get selected item for dropdown
        selected_item = mongo.db.recyclableItems.find_one(
                    {"_id": ObjectId(item_id)})["typeOfWaste"]
        # Get recyclable collections that match the selected item for
        # # accordion headers
        item_collections = list(mongo.db.itemCollections.find(
            {"itemID": ObjectId(
                item_id)}))
    # Get list of items for dropdown menu
    items = list(mongo.db.recyclableItems.find().sort("typeOfWaste"))
    # Create new dictionary of recyclable items and their matching collections
    collections_dict = list(mongo.db.itemCollections.aggregate([
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
        item_id=item_id, items=items, item_collections=item_collections,
        collections_dict=collections_dict, selected_item=selected_item,
        page_id="collections")


@app.route("/hive/members/<member_type>")
def get_recycling_members(member_type):
    if member_type == 'view-all':
        # Get selected member type for dropdown
        selected_member_type = 'Select a Member Group'
        # Get members that match the selected type for
        # # accordion headers
        member_group = list(mongo.db.hiveMembers.find(
        ))
    else:
        # Get selected member type for dropdown
        selected_member_type = member_type
        # Get members that match the selected type for
        # # accordion headers
        if member_type == 'Queen Bee':
            member_group = list(mongo.db.hiveMembers.find(
                {"isQueenBee": True}))
        elif member_type == 'Worker Bee':
            member_group = list(mongo.db.hiveMembers.find(
                {"isQueenBee": False, "isWorkerBee": True}))
        elif member_type == 'Busy Bee':
            member_group = list(mongo.db.hiveMembers.find(
                {"isQueenBee": False, "isWorkerBee": False}))
    # Check if member has collection
    members_collection = list(mongo.db.itemCollections.find(
        {}, {"memberID": 1, "_id": 0}))
    members_collection_values = list(
        [document["memberID"] for document in members_collection])
    # Create new dictionary of members and their collections
    members_dict = list(mongo.db.hiveMembers.aggregate([
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
        member_type=member_type, selected_member_type=selected_member_type,
        member_group=member_group, members_dict=members_dict,
        members_collection=members_collection,
        members_collection_values=members_collection_values, page_id="members")


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
