""" CRUD operations """

from model import db, Recipe, Ingredient, Instruction, User, User_Favorite, User_Wishlist


def create_user(fname, lname, email, password):
    """ Create and return a new user """

    user = User(fname=fname, lname=lname, email=email, password=password)

    return user



def get_all_users():
    """ Get a list of all users """

    return User.query.all()



def get_all_user_emails():
    """ Get a list of all user emails """

    user_emails = []

    for user in User.query.all():
        user_emails.append(user.email)
    

    return user_emails



def get_user_by_email(email):
    """ Returns a user with given email """

    return User.query.filter_by(email=email).one()



def get_user_by_id(id):
    """ Returns a user with given id """

    return User.query.filter_by(id=id).one()



def create_recipe(recipe_date, recipe_name, servings, notes, privacy, images, user):
    """ Create and return a new recipe """

    recipe = Recipe(recipe_date=recipe_date, recipe_name=recipe_name, servings=servings, notes=notes, privacy=privacy, images=images, user=user)

    return recipe



def get_all_recipes():
    """ Returns a list of all recipes """

    return Recipe.query.all()



def get_all_recipes_by_user(user_id):
    """ Returns all recipes created by a given user """

    return Recipe.query.filter_by(user_id=user_id).all()



def get_recipe_by_id(recipe_id):
    """ Returns a recipe with given recipe id for a given user id """

    return Recipe.query.filter_by(id = recipe_id).one()



def get_recipe_by_user_id(user_id):
    """ Returns all recipes created by a user with given user id """

    return Recipe.query.filter_by(user_id = user_id).all()



def create_ingredient(name, quantity, unit, recipe):
    """ Creates ingredient for recipe """

    ingredient = Ingredient(name=name, quantity=quantity, unit=unit, recipe=recipe)

    return ingredient



def get_all_ingredients():
    """ Returns a list of all ingredients """

    return Ingredient.query.all()



def create_instruction(step, recipe):
    """ Creates instruction step for recipe """

    instruction = Instruction(step=step, recipe=recipe)

    return instruction



def create_user_favorite(user, recipe):
    """ Create and return a new user favorite item """

    user_favorite = User_Favorite(user=user, recipe=recipe)

    return user_favorite



def get_fav_to_be_removed(user_id, recipe_id):
    """ Return user favorite to be removed with given recipe id for given user id """

    fav_to_be_removed = User_Favorite.query.filter((User_Favorite.user_id == user_id) & (User_Favorite.recipe_id == recipe_id)).one()

    return fav_to_be_removed



def get_favorites_by_user(user_id):
    """ Returns all recipes added to given user's favorites """

    user_favorites = User_Favorite.query.filter_by(user_id = user_id).all()
    
    user_favorites_recipes = []

    for favorite in user_favorites:
        user_favorites_recipes.append(favorite.recipe)
    
    return user_favorites_recipes



def create_user_wish(user, recipe):
    """ Create and return a new user wishlist item """

    user_wishlist = User_Wishlist(user=user, recipe=recipe)

    return user_wishlist



def get_wish_to_be_removed(user_id, recipe_id):
    """ Return recipe with given recipe id to be removed from wishlist for given user id """

    wish_to_be_removed = User_Wishlist.query.filter((User_Wishlist.user_id == user_id) & (User_Wishlist.recipe_id == recipe_id)).one()

    return wish_to_be_removed



def get_wishlist_by_user(user_id):
    """ Returns all recipes added to the given user's wishlist """

    user_wishlist = User_Wishlist.query.filter_by(user_id = user_id).all()

    user_wishlist_recipes = []

    for wish in user_wishlist:
        user_wishlist_recipes.append(wish.recipe)
    
    return user_wishlist_recipes






if __name__ == '__main__':
    from server import app
    connect_to_db(app)
