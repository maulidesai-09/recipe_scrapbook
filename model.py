""" Models for Recipe Scrapbook app """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """ Details of users """

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    fname = db.Column(db.String, nullable = False)
    lname = db.Column(db.String, nullable =  False)
    email = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

    recipes = db.relationship("Recipe", back_populates="user")
    favorites = db.relationship("User_Favorite", back_populates="user")
    wishlist = db.relationship("User_Wishlist", back_populates="user")


    def __repr__(self):
        """ Show info about a user """

        return f'<User_id = {self.id} User_name = {self.fname} {self.lname}>'



class Recipe(db.Model):
    """ Details of recipes """

    __tablename__ = "recipes"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    recipe_date = db.Column(db.DateTime, nullable =  False)
    recipe_name = db.Column(db.String, nullable = False, unique = True)
    servings = db.Column(db.String)
    ingredients = db.Column(db.Text, nullable = False)
    instructions = db.Column(db.Text, nullable = False)
    notes = db.Column(db.Text)
    images = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", back_populates="recipes")
    favorites = db.relationship("User_Favorite", back_populates="recipe")
    wishlist = db.relationship("User_Wishlist", back_populates="recipe")

    def __repr__(self):
        """ Show info about a recipe """

        return f'<recipe_id = {self.id}, recipe_name = {self.recipe_name}, user_id = {self.user_id}>'
    


class User_Favorite(db.Model):
    """ Details of recipe added to user's favorites """

    table_name = "user_favorites"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))

    user = db.relationship("User", back_populates="favorites")
    recipe = db.relationship("Recipe", back_populates="favorites")

    def __repr__(self):
        """ Show info about recipe added to user's favorites """

        return f'<User_favorite id = {self.id}, User_id = {self.user_id}, Recipe_id = {self.recipe_id}>'



class User_Wishlist(db.Model):
    """ Details of recipes added to user's wishlist"""

    __tablename__ = "user_wishlist"

    id = db.Column(db.Integer, autoincrement = True, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))

    user = db.relationship("User", back_populates="wishlist")
    recipe = db.relationship("Recipe", back_populates="wishlist")

    def __repr__(self):
        """ Show info about recipe added to user's wishlist """

        return f'<User_wishlist id = {self.id}, User_id = {self.user_id}, Recipe_id = {self.recipe_id}>'



def connect_to_db(flask_app, db_uri="postgresql:///recipes", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri    #location of datbase
    flask_app.config["SQLALCHEMY_ECHO"] = echo              #Enable to output the raw SQL executed by SQLAlchemy. Useful for debugging
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)





