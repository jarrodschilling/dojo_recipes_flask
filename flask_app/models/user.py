from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import user, recipe

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = "dojo_recipes_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def check_email(cls, email):
        data = {
            'email': email
        }
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) > 0:
            return False
    

    @classmethod
    def get_user(cls, data):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
            """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    

    @staticmethod
    def validate_reg(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 letters", 'reg')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 letters", 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email format", 'reg')
            is_valid = False
        if len(data['password']) < 5:
            flash("Password must be at least 5 characters long", 'reg')
            is_valid = False    
        if data['password'] != data['confirmpassword']:
            flash("Passwords must match", 'reg')
            is_valid = False
        if User.check_email(data['email']):
            flash("Email already in use, please choose another")
            is_valid = False

        return is_valid
