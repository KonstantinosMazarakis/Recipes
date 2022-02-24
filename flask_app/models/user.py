from asyncio.windows_events import NULL
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z])[a-zA-Z\d]{8,45}$')
FIRST_LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]{2,45}$')


class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.recipes = []


    @classmethod
    def create_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s ,NOW() , NOW())"
        results = connectToMySQL('recipes_schema').query_db( query, data )
        return results

    @classmethod
    def login(cls,data):
        query = "SELECT * from users WHERE email = %(email)s"
        results = connectToMySQL('recipes_schema').query_db( query, data )
        if len(results) < 1:
            return False
        return User(results[0])


    # @classmethod
    # def get_users_with_recipes(cls,data):
    #     query = "SELECT * FROM users LEFT JOIN recipes on recipes.users_id = users.id WHERE users.id = %(id)s"
    #     results = connectToMySQL('recipes_schema').query_db(query,data)
    #     user = cls(results[0])
    #     for row_from_db in results:
    #         recipe_data = {
    #             "id" : row_from_db["recipes.id"],
    #             "name" : row_from_db["name"],
    #             "description" : row_from_db["description"],
    #             "instructions" : row_from_db["instructions"],
    #             "date_made_on": row_from_db["date_made_on"],
    #             "under_30_minutes": row_from_db["under_30_minutes"],
    #             "user_id": row_from_db["user_id"],
    #             "created_at" : row_from_db["recipes.created_at"],
    #             "updated_at" : row_from_db["recipes.updated_at"]
    #         }
    #         user.recipes.append(recipe.Recipe(recipe_data))
    #     return user























    @staticmethod
    def validate_user(user):
        is_valid = True
        if not FIRST_LAST_NAME_REGEX.match(user['first_name']):
            flash("First name must be at least 2 characters and only letters.", 'create_user')
            is_valid = False
        if not FIRST_LAST_NAME_REGEX.match(user['last_name']):
            flash("Last name must be at least 2 characters and only letters.", 'create_user')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'create_user')
            is_valid = False
        if User.login(user) != False:
            flash("Email address already exist!", 'create_user')
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']):
            flash("Passwords must have a least 1 number and 1 uppercase letter and minimum of 8 digits length", 'create_user')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Password and Confirm Password has to be the same", 'create_user')
            is_valid = False
        return is_valid