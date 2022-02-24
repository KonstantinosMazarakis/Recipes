
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash



class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made_on = data['date_made_on']
        self.under_30_minutes = data['under_30_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None


    @classmethod
    def add_recipe(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, date_made_on, under_30_minutes, created_at,updated_at ,users_id ) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made_on)s, %(under_30_minutes)s ,NOW() , NOW(), %(users_id)s);"
        return connectToMySQL('recipes_schema').query_db( query, data )

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes join users on recipes.users_id = users.id;"
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for item in results:
            new_recipe = Recipe(item)

            user_data = {
                'id': item ['users.id'],
                'first_name': item ['first_name'],
                'last_name': item ['last_name'],
                'email': item ['email'],
                'password': item ['password'],
                "created_at" : item ["users.created_at"],
                "updated_at" : item ["users.updated_at"]
            }
            new_recipe.user = user.User(user_data)
            
            recipes.append(new_recipe)

        return recipes

    @classmethod
    def get_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return Recipe(results[0])


    @classmethod
    def edit_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made_on = %(date_made_on)s, under_30_minutes = %(under_30_minutes)s  WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return results


    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE  FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return results





    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("name must be at least 3 characters.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("description must be at least 3 characters.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("instructions must be at least 3 characters.")
            is_valid = False
        if recipe['date_made_on'] == "":
            flash("Please pick a date.")
            is_valid = False
        if len(recipe['under_30_minutes']) < 1:
            flash("pick 30 minutes or less.")
            is_valid = False
        return is_valid