""" CRUD operations """

from model import db, Recipe, User, User_Favorite, User_Wishlist


def create_user(fname, lname, email, password):
    """ Create and return a new user """

    user = User(fname=fname, lname=lname, email=email, password=password)

    return user



def create_recipe(recipe_date, recipe_name, servings, ingredients, instructions, notes, images, user):
    """ Create and return a new recipe """

    recipe = Recipe(recipe_date=recipe_date, recipe_name=recipe_name, servings=servings, ingredients=ingredients, instructions=instructions, notes=notes, images=images, user=user)

    return recipe



def create_user_favorite(user, recipe):
    """ Create and return a new user favorite item """

    user_favorite = User_Favorite(user=user, recipe=recipe)

    return user_favorite



def create_user_wishlist(user, recipe):
    """ Create and return a new user wishlist item """

    user_wishlist = User_Wishlist(user=user, recipe=recipe)

    return user_wishlist







if __name__ == '__main__':
    from server import app
    connect_to_db(app)
