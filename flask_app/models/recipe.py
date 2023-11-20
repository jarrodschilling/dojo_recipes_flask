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
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO recipes (name, description, instructions, date_made, under) 
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under)s,);"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all(cls, data):
        query = """SELECT * FROM recipes WHERE user_id = %(user_id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes
    
    @classmethod
    def delete_one(cls, data):
        query = """DELETE FROM recipes WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query(query, data)
    

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