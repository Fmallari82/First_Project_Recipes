from fileinput import filename
import re
from flask_app.config.mysqlconnection import  connectToMySQL
# model the class after the friend table from our database
from flask_app import  DATABASE
from flask_app import flash, session
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_app.models import model_user, model_recipe

class Image:
    db = DATABASE
    recipe = []
    def __init__( self , data ):
        self.id = data['id']
        self.file_name = data['file_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO images (file_name) VALUES (%(file_name)s );"
        image_id = connectToMySQL(DATABASE).query_db(query, data)
        print (image_id)
        return image_id

    @classmethod
    def get_all(cls): #to view all ids
        query = "SELECT * FROM images;"
        result = connectToMySQL(DATABASE).query_db(query)
        #set variable to an empty list
        images = []
        #for the row in "result" or the database query on workbench apend to empty list
        for row in result:
            images.append(cls(row))

        #to check for errors
        if not result:
            return False
        #return list with row from database query to function
        return images

    @classmethod
    def get_one(cls, data): #to select/view individual id
        query ="SELECT * FROM images WHERE images.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query , data )
        # results will be a list of object for specific id
        print(results)
        if not results:
            return False
        return cls(results[0])