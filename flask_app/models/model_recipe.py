
import re
from flask_app.config.mysqlconnection import  connectToMySQL
# model the class after the friend table from our database
from flask_app import  DATABASE
from flask_app import flash, session
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_app.models import model_user, model_image

class Recipe:
    db = DATABASE
    user = []
    image = []
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.image = data['file']
        self.name = data['name']
        self.ingredients = data['ingredients']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    #CREATE
    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (user_id, file, name, ingredients,instructions) VALUES (%(user_id)s, %(file)s,%(name)s,%(ingredients)s,%(instructions)s);"
        recipe_id = connectToMySQL(DATABASE).query_db(query, data)
        print (recipe_id)
        return recipe_id

    #READ
    #to view all ids
    @classmethod
    def get_all(cls):
        #query join to get to instances that belong together by setting users.id to equal user_id 
        query ="SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        #return a lists of dictionaries
        results = connectToMySQL(DATABASE).query_db( query )

        if not results:
            return []

        #set variable to empty list
        all_recipe = []
        for dict in results:
            #set variable of new instance that will be created from joining to instances
            recipe_instance = cls(dict)
            #set new variable to = values in instance that was joined to current instance/model
            user_data = {
                #** dict is all values in new instance from join
                **dict,
                #list all values with same ids from both instances
                "id" : dict["users.id"],
                "created_at" : dict["users.created_at"],
                "updated_at" : dict["users.created_at"]
            }
            #set new variable of name of joining instance to equal the new joined instance
            user_instance = model_user.User(user_data)
            #assigning an attribute called owner(in this case) -> points to a user instance
            #append the empty list to include all values of the new joined instance
            all_recipe.append(recipe_instance)
            recipe_instance.owner = user_instance
        #returns a list of instances
        return all_recipe

    
    @classmethod
    def get_one(cls, data): #to select/view individual id
        query ="SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query , data )
        print(results)
        if not results:
            return False
        
        recipe_instance = cls(results[0])
        for dict in results:
            user_data = {
                **dict,
                "id" : dict["users.id"],
                "created_at" : dict["users.created_at"],
                "updated_at" : dict["users.created_at"]
            }
        recipe_instance.creator = model_user.User(user_data)
        return recipe_instance

    #UPDATE    
    @classmethod
    def update_one(cls,data):
        query = "UPDATE recipes SET name=%(name)s, ingredients=%(ingredients)s, instructions=%(instructions)s, image = %(image)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #DELETE
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        
        if not result:
            return False
        # return an instance
        return result


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 1:
            is_valid = False
            flash("Name must not be blank.", 'err_recipe_name')

        # if len(recipe['ingredients']) < 1:
        #     is_valid = False
        #     flash("ingredients must not be blank.", 'err_recipe_ingredients')
        if len(recipe['ingredients']) < 1:
            is_valid = False
            flash("Ingredients must not be blank.", 'err_recipe_ingredients')
        
        if len(recipe['instructions']) < 1:
            is_valid = False
            flash("Instructions must not be blank.", 'err_recipe_instructions')
        
        return is_valid
        
    @staticmethod
    def validate_recipe_edit(recipe):
        is_valid = True
        if len(recipe['name']) < 1:
            is_valid = False
            flash("Name must not be blank.", 'err_recipe_name_edit')

        if len(recipe['ingredients']) < 1:
            is_valid = False
            flash("ingredients must not be blank.", 'err_recipe_ingredients_edit')
        
        if len(recipe['instructions']) < 1:
            is_valid = False
            flash("Instructions must not be blank.", 'err_recipe_instructions_edit')
        
        return is_valid