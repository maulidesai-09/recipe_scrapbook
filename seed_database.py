""" Script to seed database """

import os
import json     #in case you want to load data from a json file (most likely won't be used for this project)
from random import choice, randint
from datetime import datetime

import crud
import model
import server


os.system("dropdb recipes")
os.system("createdb recipes")

model.connect_to_db(server.app)
server.app.app_context().push()
model.db.create_all()


### Creating Recipes using CRUD functions ###

# for n in range(11):



### Creating Users, User Favorites and User Wishlist using CRUD functions ###

users_in_db = []
recipes_in_db = []
n_recipe = 1


for n in range(1,11):
    fname = f"Fname{n}"
    lname = f"Lname{n}"
    email = f"test{n}@test.com"
    password = f"test{n}"

    db_user = crud.create_user(fname, lname, email, password)
    model.db.session.add(db_user)
    users_in_db.append(db_user)

    # recipes_in_db = []

    for m in range(n_recipe, n_recipe+6):
        recipe_date = datetime.now()
        recipe_name = f"Recipe_test_{m}"
        servings = m
        ingredients = f"Ingredients_test_{m}"
        instructions = f"Instructions_test_{m}"
        notes = f"Notes_test_{m}"
        images = f"Images_test_{m}"
        user = db_user

        db_recipe = crud.create_recipe(recipe_date, recipe_name, servings, 
                                       ingredients, instructions, notes, 
                                       images, user)
        model.db.session.add(db_recipe)
        # model.db.session.commit()  #Committing here because we need a list of all recipes to create user_fav and user_wish below
        recipes_in_db.append(db_recipe)
    
    n_recipe += 6
        
    
    for n in range(6):
        user = db_user
        recipe_fav = choice(recipes_in_db)
        recipe_wish = choice(recipes_in_db)

        db_user_favorite = crud.create_user_favorite(user, recipe_fav)
        model.db.session.add(db_user_favorite)

        db_user_wishlist = crud.create_user_wishlist(user, recipe_wish)
        model.db.session.add(db_user_wishlist)

    
    model.db.session.commit()
    










