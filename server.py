"""Server for recipe scrapbook app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud, re
from jinja2 import StrictUndefined
import os
import json
from datetime import date
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "recipescrapbook"
app.jinja_env.undefined = StrictUndefined

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# client = OpenAI()
# equivalent to: API_KEY = os.environ['OPENAI_API_KEY'] - done in Parks project

# client = OpenAI(api_key="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")

@app.route("/")
def homepage():
    """ View homepage (login page) """

    return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    """ Log in an existing user """

    email = request.form.get("email")
    password = request.form.get("password")

    user_emails = crud.get_all_user_emails()
    print("############################## user_emails = ", user_emails)

    if email in user_emails:
        user = crud.get_user_by_email(email)
        if user.password == password:
            session["user_email"] = user.email
            flash(f"Logged in successfully - {user.fname} {user.lname}")
            return redirect(f"/login/{user.id}")
        
        else:
            flash("The password you entered is incorrect. Please try again.")
            return redirect("/")
    
    else:
        flash("Account with this email not found. Please sign up to create a new account for this email.")
        return redirect("/")


@app.route("/signup",  methods=["POST", "GET"])
def signup():
    """ Sign up a new user """

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user_emails = crud.get_all_user_emails()
    print("############################## user_emails = ", user_emails)

    if email in user_emails:
        flash("An account with this email already exists. Please log in as an existing user or create a new account using a different email.")
        return redirect("/")
    else:
        new_user = crud.create_user(fname, lname, email, password)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Congrats! Account created for {new_user.fname} {new_user.lname}!")

        return redirect(f"/login/{new_user.id}")
    

@app.route("/login/<int:user_id>")
def user_homepage(user_id):
    """ Display homepage for logged in user """

    user = crud.get_user_by_id(user_id)

    return render_template("user_homepage.html", user=user)


@app.route("/login/<int:user_id>/new_recipe")
def new_recipe(user_id):
    """ Display form for adding new recipe """

    # print("########### user_id = ", user_id)

    user = crud.get_user_by_id(user_id)

    return render_template("add_recipe.html", user=user)



@app.route("/login/<int:user_id>/new_recipe/add_recipe", methods=["POST"])
def add_recipe(user_id):
    """ Saves new recipe added by user """

    # print("########### user_id = ", user_id, type(user_id))

    user = crud.get_user_by_id(user_id)

    # print("######################################", request.form)

    recipe_date = request.json.get("recipe_date")
    print("########date = ", recipe_date)
    recipe_name = request.json.get("recipe_name")
    servings = request.json.get("servings")
    notes = request.json.get("notes")
    privacy = request.json.get("privacy")
    recipe_id = request.json.get("recipe_id")

    print("############## recipe_id = ", recipe_id)
    print("############## privacy = ", privacy)

    images = "Image Appears Here"

    ### Code to save a new recipe
    if recipe_id == "new_recipe":
        recipe_to_save = crud.create_recipe(recipe_date=recipe_date, recipe_name=recipe_name, 
                                            servings=servings, notes=notes, privacy=privacy, images=images, 
                                            user=user)
        db.session.add(recipe_to_save)
        db.session.commit()

    ### Code to save/ update edited recipe
    else:
        recipe_to_save = crud.get_recipe_by_id(recipe_id)
        recipe_to_save.recipe_date = recipe_date
        recipe_to_save.recipe_name = recipe_name
        recipe_to_save.servings = servings
        recipe_to_save.notes = notes
        recipe_to_save.privacy = privacy

        ## Delete old ingredients
        for ingredient in recipe_to_save.ingredients:
            db.session.delete(ingredient)
        
        ## Delete old instructions
        for instruction in recipe_to_save.instructions:
            db.session.delete(instruction)
        
        db.session.commit()


    ### get details of ingredients from AJAX POST request and save to database
    ingredient_list = request.json.get("ingredients")

    # print("################## ingredient_list", ingredient_list)

    for ingredient in ingredient_list:
        # print("####### ingredient = ", ingredient)
        ingredient_name = ingredient["name"]
        ingredient_quantity = ingredient["quantity"]
        ingredient_unit = ingredient["unit"]

        ingredient_to_save = crud.create_ingredient(name=ingredient_name, 
                                                    quantity=ingredient_quantity,
                                                    unit=ingredient_unit,
                                                    recipe=recipe_to_save)
        
        db.session.add(ingredient_to_save)
        db.session.commit()


    ### get details of instructions from AJAX post request and save to database
    instruction_list = request.json.get("instructions")

    for instruction in instruction_list:
        step = instruction["description"]

        instruction_to_save = crud.create_instruction(step=step, recipe=recipe_to_save)
        
        db.session.add(instruction_to_save)
        db.session.commit()
    

    return jsonify(recipe_to_save.id)



@app.route("/login/<int:user_id>/saved_recipe/<int:recipe_id>")
def display_saved_recipe(user_id, recipe_id):
    """ Displays saved recipe with given recipe id for given user """

    # print("####### recipe id = ", recipe_id)

    user = crud.get_user_by_id(user_id)

    recipe = crud.get_recipe_by_id(recipe_id)

    print("########## recipe_date = ", recipe.recipe_date)

    return render_template("saved_recipe.html", recipe = recipe, user=user)



@app.route("/login/<int:user_id>/saved_recipe/<int:recipe_id>/add_to_fav")
def add_recipe_to_fav(user_id, recipe_id):
    """ Adds recipe with given id to favorites for given user """

    user = crud.get_user_by_id(user_id)
    recipe = crud.get_recipe_by_id(recipe_id)
    user_favorites = crud.get_favorites_by_user(user_id)
    print("############user_favorites = ", user_favorites)

    if recipe in user_favorites:
        flash("Recipe already added to favorites")
    else:
        new_favorite = crud.create_user_favorite(user=user, recipe=recipe)

        db.session.add(new_favorite)
        db.session.commit()
        flash("Added to favorites!")

    return redirect(f"/login/{user_id}/saved_recipe/{recipe_id}")



@app.route("/login/<int:user_id>/favorite_recipes")
def view_user_favorites(user_id):
    """ View a list of recipes added to given user's favorites """

    user = crud.get_user_by_id(user_id)
    user_favorite_recipes = crud.get_favorites_by_user(user_id)

    return render_template("user_favorites.html", user=user, user_favorite_recipes=user_favorite_recipes)



@app.route("/login/<int:user_id>/saved_recipe/<int:recipe_id>/remove_fav")
def remove_recipe_from_fav(user_id, recipe_id):
    """ Removes recipe with given id from favorites for given user """

    user = crud.get_user_by_id(user_id)
    recipe = crud.get_recipe_by_id(recipe_id)

    fav_to_be_removed = crud.get_fav_to_be_removed(user_id, recipe_id)
    # print("##########fav_to_be_removed = ", fav_to_be_removed)
    fav_to_be_removed_name = fav_to_be_removed.recipe.recipe_name

    db.session.delete(fav_to_be_removed)
    db.session.commit()

    flash(f"{fav_to_be_removed_name} removed from favorites")

    return redirect(f"/login/{user_id}/favorite_recipes")



@app.route("/login/<int:user_id>/saved_recipe/<int:recipe_id>/add_to_wish")
def add_recipe_to_wish(user_id, recipe_id):
    """ Adds recipe with given id to wishlist for given user """

    user = crud.get_user_by_id(user_id)
    recipe = crud.get_recipe_by_id(recipe_id)
    user_wishlist = crud.get_wishlist_by_user(user_id)

    if recipe in user_wishlist:
        flash("Recipe already added to wishlist")
    else:
        new_wish = crud.create_user_wish(user=user, recipe=recipe)

        db.session.add(new_wish)
        db.session.commit()
        flash("Added to wishlist!")
    
    return redirect(f"/login/{user_id}/saved_recipe/{recipe_id}")



@app.route("/login/<int:user_id>/wishlist_recipes")
def view_user_wishlist(user_id):
    """ View a list of recipes added to given user's wishlist """

    user = crud.get_user_by_id(user_id)
    user_wishlist_recipes = crud.get_wishlist_by_user(user_id)


    print("######## user_id = ", user.id)
    print("######### recipes = ", user_wishlist_recipes)

    return render_template("user_wishlist.html", user=user, user_wishlist_recipes=user_wishlist_recipes)



@app.route("/login/<int:user_id>/saved_recipe/<int:recipe_id>/remove_wish")
def remove_recipe_from_wishlist(user_id, recipe_id):
    """ Removes recipe with given id from wishlist for given user """

    user = crud.get_user_by_id(user_id)
    recipe = crud.get_recipe_by_id(recipe_id)

    wish_to_be_removed = crud.get_wish_to_be_removed(user_id, recipe_id)
    
    wish_to_be_removed_name = wish_to_be_removed.recipe.recipe_name

    db.session.delete(wish_to_be_removed)
    db.session.commit()

    flash(f"{wish_to_be_removed_name} removed from wishlist")

    return redirect(f"/login/{user_id}/wishlist_recipes")



@app.route("/login/<int:user_id>/my_recipes")
def my_recipes(user_id):
    """ Displays a list of all recipes created by a given user """
    user = crud.get_user_by_id(user_id)

    my_recipes = crud.get_recipe_by_user_id(user_id)

    return render_template("my_recipes.html", user=user, my_recipes=my_recipes)


@app.route("/login/<int:user_id>/all_recipes")
def all_recipes(user_id):
    """ Displays all recipes by logged in user + public recipes by other users)"""

    user = crud.get_user_by_id(user_id)
    all_recipes = crud.get_all_recipes()
    all_recipes_by_user = crud.get_all_recipes_by_user(user_id)
    
    # ### Get all recipes that are public from all users
    # all_recipes_public = []
    # for recipe in all_recipes:
    #     if recipe.privacy == "Public Recipe":
    #         all_recipes_public.append(recipe)
    
    # ### Add recipes by user (to include private recipes by logged in user; 
    #     # duplication later removed by converting list to set)
    # all_recipes_public.extend(all_recipes_by_user)

    # print("####### all recipes public = ", all_recipes_public)
    
    # ### Convert list to set to remove duplication of public recipes by user 
    #     # (which would be included in boyh all_recipes and all_recipes_by_user)
    # all_recipes_public_set = set(all_recipes_public)

    all_recipes_public = []

    for recipe in all_recipes:
        if recipe.privacy == "Public Recipe" and recipe.user != user:
            all_recipes_public.append(recipe)

    return render_template("all_recipes.html", user=user, 
                           all_recipes_public=all_recipes_public,
                           all_recipes_by_user=all_recipes_by_user)



@app.route("/login/<user_id>/saved_recipe/<int:recipe_id>/edit_recipe")
def edit_recipe(user_id, recipe_id):
    """ Displays form with pre-filled data for editing a given recipe """

    user = crud.get_user_by_id(user_id)

    recipe = crud.get_recipe_by_id(recipe_id)
    # print("##### recipe.privacy = ", recipe.privacy)

    return render_template("edit_recipe.html", user=user, recipe=recipe)



@app.route("/login/<int:user_id>/<int:recipe_id>/delete_recipe")
def delete_recipe(user_id, recipe_id):
    """ Deletes a recipe with given recipe id for given user id """

    user = crud.get_user_by_id(user_id)
    recipe_to_be_deleted = crud.get_recipe_by_id(recipe_id)
    source_url = request.referrer

    print("########## recipe_to_be_deleted = ", recipe_to_be_deleted)

    ("####### source url =", source_url)

    confirmation = request.args.get("confirmation")

    if confirmation == "Yes":
        db.session.delete(recipe_to_be_deleted)
        db.session.commit()
        flash("Recipe deleted")
        if source_url == f"/login/{user_id}/saved_recipe/{recipe_id}":
            return redirect(f"/login/{user_id}")
        else:
            return redirect(source_url)
        
    else:
        flash("Recipe not deleted")
        return redirect(source_url)



@app.route("/login/<int:user_id>/search")
def search_for_a_recipe(user_id):
    """ Returns the search form """

    user = crud.get_user_by_id(user_id)

    return render_template("search.html", user=user)



@app.route("/login/<int:user_id>/search/search_results")
def display_search_results(user_id):
    """ Returns search results """

    user = crud.get_user_by_id(user_id)
    search_type = request.args.get("search_radio")
    search_input = request.args.get("search_input")
    search_privacy = request.args.get("search_radio_privacy")

    print("###### search_privacy = ", search_privacy)

    print("######### search radio=", search_type)
    print("######### search input=", search_input)
    print(type(search_input))

    ### removing extra space (substituting 1+ space with just 1 space) from search_input using 
        # 're'(Regular Expressions) module
    search_input = re.sub(" +"," ",search_input)

    ### removing non-alphabetic & non-numeric characters and converting the string (search_input) 
        # to a list using 're' (Regular Expressions) module

    search_input_list = re.split("`|~|!|@|#|\$|%|\^|&|\*|\(|\)|-|_|=|\+|{|}|\[|\]|\||\\\|;|:|'|\"|,|<|\.|>|/|\?| ", search_input)

    for item in search_input_list:
        if len(item) == 0:
            search_input_list.remove(item)

    print("######### search_input_list =", search_input_list)

    #### PERSONAL RECIPES SEARCH (search results include only the recipes created by the user) ####

    if search_privacy == "search_private":
        search_privacy = "Private Recipes"

        ### Get all recipes created by user
        all_recipes_private = crud.get_all_recipes_by_user(user_id)

        all_recipes_private_set = set(all_recipes_private)
        
        search_input_set = set(search_input_list)

        result_recipes_by_user = set()
        result_recipes_public = set()

        if search_type == "recipe_name":
            search_type_name = "Recipe Name"
            for item in search_input_set:
                for recipe in all_recipes_private_set:
                    if item.lower() in recipe.recipe_name.lower():
                        result_recipes_by_user.add(recipe)
        else:
            search_type_name = "Recipe Ingredients"
            for item in search_input_set:
                # print("######### item = ",item)
                for recipe in all_recipes_private_set:
                    # print("######### ingredients = ",recipe.ingredients)
                    for ingredient in recipe.ingredients:
                        if item.lower() in ingredient.name.lower():
                            result_recipes_by_user.add(recipe)


     #### PUBLIC RECIPES SEARCH (search results include the recipes created by the user as well as 
        # recipes created by other users that are public) ####

    if search_privacy == "search_public":
        search_privacy = "Public Recipes"

        ### Get all recipes by all users
        all_recipes = crud.get_all_recipes()
        # print("####### all_recipes = ", all_recipes)
        # sample = all_recipes[-1]
        # print("######## sample.privacy = ", sample.privacy)

        ### Get all recipes created by user
        all_recipes_by_user = crud.get_all_recipes_by_user(user_id)
        # print("####### all_recipes_by_user = ", all_recipes_by_user)
        
        ### Get all recipes that are public from all users
        all_recipes_public = []
        for recipe in all_recipes:
            if recipe.privacy == "Public Recipe":
                all_recipes_public.append(recipe)
        
        ### Add recipes by user (to include private recipes by logged in user; 
            # duplication later removed by converting list to set)
        all_recipes_public.extend(all_recipes_by_user)

        print("####### all recipes public = ", all_recipes_public)
        
        ### Convert list to set to remove duplication of public recipes by user 
            # (which would be included in boyh all_recipes and all_recipes_by_user)
        all_recipes_public_set = set(all_recipes_public)
        
        search_input_set = set(search_input_list)

        result_recipes_public = set()
        result_recipes_by_user = set()

        if search_type == "recipe_name":
            search_type_name = "Recipe Name"
            for item in search_input_set:
                for recipe in all_recipes_public_set:
                    if item.lower() in recipe.recipe_name.lower():
                        if recipe.user == user:
                            result_recipes_by_user.add(recipe)
                        else:
                            result_recipes_public.add(recipe)
        else:
            search_type_name = "Recipe Ingredients"
            for item in search_input_set:
                # print("######### item = ",item)
                for recipe in all_recipes_public_set:
                    # print("######### ingredients = ",recipe.ingredients)
                    for ingredient in recipe.ingredients:
                        if item.lower() in ingredient.name.lower():
                            if recipe.user == user:
                                result_recipes_by_user.add(recipe)
                            else:
                                result_recipes_public.add(recipe)
    

    # print("####### result = ",result_recipes)


    return render_template("search_result.html", 
                           search_input = search_input, 
                           search_type_name = search_type_name, 
                           search_privacy = search_privacy,
                           user = user, 
                           result_recipes_by_user = result_recipes_by_user,
                           result_recipes_public = result_recipes_public)

        


@app.route("/login/<int:user_id>/logout")
def logout(user_id):
    """ Logs out a user """

    user = crud.get_user_by_id(user_id)
    confirmation = request.args.get("confirmation")

    # print("##################### session = ", session)
    # print("#############", user.email)

    # print("###############confirmation = ", confirmation)
    
    if confirmation == "Yes":
        del session["user_email"]
        flash("Logged out successfully!")
        # print("##################### session = ", session)
        
        return redirect("/")
    else:
        flash("You have not been logged out")
        return redirect(request.referrer)




######### OPENAI API GENERATED RECIPES #############

@app.route("/login/<int:user_id>/ai_recipe_input/")
def ai_recipe_input(user_id):
    """ Displays form to enter ingredients to generate recipe using OpenAI API"""

    user = crud.get_user_by_id(user_id)

    return render_template("ai_recipe_input.html", user=user)



@app.route("/login/<int:user_id>/ai_recipe_input/ai_recipe_result")
def generate_ai_recipe(user_id):
    """ Generates and displays recipe generated by OpenAI API by using ingredients entered by user"""

    user = crud.get_user_by_id(user_id)
    input_ingredients = request.args.get("ai_ingredients")

    # ######## The following steps are to format the input ingredients to a list after 
    #     # removing extra spaces and non alpha-numeric characters. However, it is 
    #     # not required since OpenAI API does not need it in such a clean format.
    
    # ### removing extra space (substituting 1+ space with just 1 space) from input_ingredients using 
    #     # 're'(Regular Expressions) module
    # input_ingredients = re.sub(" +"," ",input_ingredients)

    # ### removing non-alphabetic & non-numeric characters and converting the string (search_input) 
    #     # to a list using 're' (Regular Expressions) module

    # input_ingredients_list = re.split("`|~|!|@|#|\$|%|\^|&|\*|\(|\)|-|_|=|\+|{|}|\[|\]|\||\\\|;|:|'|\"|,|<|\.|>|/|\?| ", input_ingredients)

    # for item in input_ingredients_list:
    #     if len(item) == 0:
    #         input_ingredients_list.remove(item)

    input_ingredients_list = input_ingredients


    print("######### input_ingredients_list =", input_ingredients_list)

    #### Making API call

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON. Do not include line breaks '/n' in the result."},
        {"role": "system", "content": """Please use the following format to generate json output: {
            "title": "[Your Recipe Title]",
            "servings": "[Specify the number of servings]",
            "ingredients": {
                "Ingredient 1 Name": ["Ingredient Quantity Without Unit", "Ingredient Quantity Unit"],
                "Ingredient 2 Name": ["Ingredient Quantity Without Unit", "Ingredient Quantity Unit"],
                "Ingredient 4 Name": ["Ingredient Quantity Without Unit", "Ingredient Quantity Unit"],
                ...
            },
            "instructions": [
                "[Step 1 without step number]",
                "[Step 2 without step number]",
                "[Step 3 without step number]",
                ...
            ],
            "notes": "[Any extra information or tips]"
            }"""},
        {"role": "user", "content": f"Create a recipe using the ingredients: {input_ingredients_list}. Please breakdown the recipe "}
        ]
    )

    result_nonjson = completion.choices[0].message.content
    api_call_finish_reason = print(completion.choices[0].finish_reason)

    result = json.loads(result_nonjson)
    # print(result)
    # print(result["title"])
    # print(type(result))

    recipe_date = str(date.today())
    recipe_name = result["title"]
    servings = result["servings"]
    ingredients = result["ingredients"]
    instructions = result["instructions"]
    notes = result["notes"]
    privacy = "Private Recipe" 

    return render_template("ai_recipe_result.html", 
                           user=user, 
                           recipe_date = recipe_date, 
                           recipe_name = recipe_name,
                           servings = servings,
                           ingredients = ingredients,
                           instructions = instructions,
                           notes = notes,
                           privacy = privacy,
                           api_call_finish_reason=api_call_finish_reason)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)