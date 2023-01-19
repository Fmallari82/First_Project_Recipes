
import re
from flask_app.config.mysqlconnection import  connectToMySQL
# model the class after the friend table from our database
from flask_app import  bcrypt, DATABASE
from flask_app import flash, session
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

#create model/instance 
class User:
    #shorthand for DATABSE to be called on by validator function
    db = DATABASE
    #set all values for instance that is being created 
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.fullname = f"{self.first_name()} {self.last_name()}"
    # Now we use class methods to query our database
        self.recipes=[]
    
    #CREATE
    @classmethod
    def create(cls, data):
        #set query to insert. Verify with workbench to make sure it is working
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        #set user_id to connect to database on workbench
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        print (user_id)
        return user_id
    
    #READ
    @classmethod
    def get_all(cls): #to view all ids
        query = "SELECT * FROM users;"
        result = connectToMySQL(DATABASE).query_db(query)
        #set variable to an empty list
        users = []
        #for the row in "result" or the database query on workbench apend to empty list
        for row in result:
            users.append(cls(row))

        #to check for errors
        if not result:
            return False
        #return list with row from database query to function
        return users

    #to verify if email exist
    @classmethod
    def get_one_by_email(cls, data): #to verify email exist
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        
        if not result:
            return False
        if len(result) < 1:
            return False
        
        # return an instance
        return cls(result[0])

    #to query single id
    @classmethod
    def get_one(cls, data): #to select/view individual id
        query ="SELECT * FROM users WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query , data )
        # results will be a list of object for specific id
        print(results)
        if not results:
            return False
        return cls(results[0])

    #to validate
    @staticmethod 
    def validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(user['first_name']) < 3:
            is_valid = False
            flash("First name must be at least 3 characters.", 'err_user_first_name')
        if len(user['last_name']) < 3:
            is_valid = False
            flash("Last name must be at least 3 characters.",'err_user_last_name')
        if len(user['email']) < 3:
            is_valid = False
            flash("Email must be at least 3 characters.", 'err_user_email')
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!" , 'err_user_email')
        if len(results) >= 1:
            flash('Email already taken.' , 'err_user_email')
            is_valid = False
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be at least 3 charactes.", 'err_user_password')
        if user['confirm_password'] != user['password']:
            is_valid = False
            flash("Passwords do not match", 'err_user_password')
        return is_valid

    #UPDATE
    @classmethod
    def update_one(cls):
        pass
    
    #DELETE
    @classmethod
    def delete_one(cls):
        pass

    @staticmethod
    def validate_login(user):
        is_valid = True
        
        if len(user['email']) < 3:
            is_valid = False
            flash("Email must be at least 3 characters.", 'err_user_email_login')
        
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!" , 'err_user_email_login')
            is_valid = False

        if len(user['password']) < 3:
            is_valid = False
            flash("Password must be at least 3 charactes.", 'err_user_password_login')
        
        if is_valid:
            potential_user = User.get_one_by_email({'email': user['email']})
            if not potential_user:
                is_valid = False
                flash('Email is not found', 'err_user_email_login')
            else:
                # validate the password
                if not bcrypt.check_password_hash(potential_user.password, user['password']):
                    is_valid = False
                    flash('Invalid Password', 'err_user_password_login')
                else:
                    session['user_id'] = potential_user.id
        return is_valid