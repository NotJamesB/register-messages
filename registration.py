from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
    


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('login_reg').query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('login_reg').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('login_reg').query_db(query, data)

    @classmethod
    def show(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('login_reg').query_db(query)
        users = []
        for row in results:
            users.append( cls(row) )
        return users

    @staticmethod
    def validate_login(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email =%(email)s"
        results = connectToMySQL('login_reg').query_db(query,user)
        return is_valid

    @staticmethod
    def validate_reg(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email =%(email)s;"
        results = connectToMySQL('login_reg').query_db(query,user)
        if len(results) >= 1:
            flash("Email is taken")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email!")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be more than 3 characters")
            is_valid=False
        if len(user['last_name']) < 3:
            flash("Last name must be more than 3 characters")
            is_valid=False
        if len(user['password']) < 7:
            flash("password be more than 6 characters")
            is_valid=False
        if user['password'] != user['confirm']:
            flash("Passwords must match.")
            is_valid = False
        return is_valid