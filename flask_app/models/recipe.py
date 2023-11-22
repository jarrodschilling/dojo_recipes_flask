from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import user, recipe

class Recipe:
    db = "dojo_recipes_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under = data['under']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_cook = None
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO recipes (name, description, instructions, date_made, under, user_id) 
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under)s, %(user_id)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM recipes WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all(cls, data):
        query = """SELECT * FROM recipes
                LEFT JOIN users ON users.id = recipes.user_id;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        recipes = []
        for row in results:
            one_recipe = cls(row)
            recipe_cook_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }

            cook = user.User(recipe_cook_info)
            one_recipe.user_cook = cook
            recipes.append(one_recipe)

        return recipes
    
    @classmethod
    def delete_one(cls, data):
        query = """DELETE FROM recipes WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def update_recipe(cls, data):
        query = """UPDATE recipes SET name = %(name)s, description = %(description)s, 
                instructions = %(instructions)s, date_made = %(date_made)s, 
                under = %(under)s WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters")
            is_valid = False
        if len(data['date_made']) < 1:
            flash("Must enter a valid date")
            is_valid = False

        return is_valid